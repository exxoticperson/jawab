const twilio = require('twilio');
const { loadClinicConfig } = require('../config/tenants');
const { processIncomingMessage } = require('../services/conversationEngine');

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const handleIncomingCall = async (req, res) => {
    const { To, From, CallStatus } = req.body;
    
    // We only care if it's missed/no-answer or if we're setting up the webhook to just reject and text
    const clinicConfig = loadClinicConfig(To);
    console.log(`Missed call detected from ${From} to clinic ${clinicConfig.name}`);

    // Send initial bilingual WhatsApp message via Twilio API
    setTimeout(async () => {
        try {
            await client.messages.create({
                body: `🇦🇪 مرحباً! لاحظنا أنك اتصلت — كيف يمكننا مساعدتك في حجز موعد؟\n\n🇬🇧 Hi! We noticed you called — how can we help you book an appointment?`,
                from: process.env.TWILIO_WHATSAPP_NUMBER,
                to: `whatsapp:${From}`
            });
            console.log(`Sent missed call recovery WhatsApp to ${From}`);
        } catch (error) {
            console.error('Error sending WhatsApp message:', error);
        }
    }, 5000); // Small delay to seem natural after hanging up

    // Twiml response for the call itself: hang up (or play a short message if answering)
    const twiml = new twilio.twiml.VoiceResponse();
    twiml.reject({ reason: 'busy' });
    res.type('text/xml').send(twiml.toString());
};

const handleIncomingWhatsApp = async (req, res) => {
    const { To, From, Body } = req.body;
    
    // In production To will be WhatsApp format "whatsapp:+1..."
    const clinicConfig = loadClinicConfig(To.replace('whatsapp:', ''));
    
    const responseText = await processIncomingMessage(From, Body, clinicConfig);
    
    const twiml = new twilio.twiml.MessagingResponse();
    twiml.message(responseText);
    res.type('text/xml').send(twiml.toString());
};

module.exports = { handleIncomingCall, handleIncomingWhatsApp };
