const express = require('express');
const dotenv = require('dotenv');
const twilio = require('twilio');
const { handleIncomingCall, handleIncomingWhatsApp } = require('./controllers/webhooks');

dotenv.config();

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Twilio webhook endpoints
app.post('/webhook/call', handleIncomingCall);
app.post('/webhook/whatsapp', handleIncomingWhatsApp);

// Health check
app.get('/health', (req, res) => res.status(200).send('Jawab Backend is running'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Jawab server running on port ${PORT}`);
});
