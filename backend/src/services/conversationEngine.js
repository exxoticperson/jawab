const { getLocalizedResponse, isEnglishText } = require('../utils/dialectAdapter');
const { generateBookingLink } = require('./bookingService');
const { logConversation } = require('./csvLogger');

// In-memory state store for MVP (use Redis/DB in prod)
const userStates = {};

const processIncomingMessage = async (fromNumber, messageBody, clinicConfig) => {
    // 1. Determine Language
    const isEnglish = isEnglishText(messageBody);

    // 2. State Retrieval & Initialization
    if (!userStates[fromNumber]) {
        // If this is the patient's first reply, we ask for their name
        userStates[fromNumber] = { step: 'ASK_NAME', isEnglish };
        return getLocalizedResponse('askName', isEnglish);
    }
    
    const state = userStates[fromNumber];
    // Lock in their language preference after first message, 
    // unless they switch explicitly, but we'll stick to their first detected language for simplicity
    const currentLangIsEnglish = state.isEnglish;

    // 3. Fallback / Intent Override (Handoff trigger)
    // If they ask a complex question or pricing, skip to handoff
    if (messageBody.match(/(price|cost|insurance|كم|بكم|تأمين)/i)) {
        if (state.step !== 'HANDOFF') {
            state.step = 'HANDOFF';
            logConversation(clinicConfig.clinicId, fromNumber, currentLangIsEnglish ? 'EN' : 'AR', 'HANDOFF_REQUESTED');
            return getLocalizedResponse('handoff', currentLangIsEnglish);
        }
    }

    // 4. State Machine Routing
    if (state.step === 'ASK_NAME') {
        state.name = messageBody;
        state.step = 'ASK_ISSUE';
        return getLocalizedResponse('askIssue', currentLangIsEnglish);
        
    } else if (state.step === 'ASK_ISSUE') {
        state.issue = messageBody;
        state.step = 'PROVIDE_LINK';
        
        // Final booking step
        const link = await generateBookingLink(clinicConfig);
        logConversation(clinicConfig.clinicId, fromNumber, currentLangIsEnglish ? 'EN' : 'AR', 'BOOKING_LINK_SENT');
        
        return getLocalizedResponse('provideLink', currentLangIsEnglish) + `\n${link}`;
        
    } else if (state.step === 'PROVIDE_LINK' || state.step === 'HANDOFF') {
        return getLocalizedResponse('alreadyHandled', currentLangIsEnglish);
    }

    // Fallback reset
    return getLocalizedResponse('greeting', currentLangIsEnglish);
};

module.exports = { processIncomingMessage };
