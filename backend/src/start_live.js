const localtunnel = require('localtunnel');
const { spawn } = require('child_process');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();
const PORT = process.env.PORT || 3000;

// Start the Express server
console.log('🚀 Booting Jawab Backend...');
const serverProcess = spawn('node', [path.join(__dirname, 'index.js')], {
    stdio: 'inherit', // Streams logs directly to terminal
    env: process.env
});

// Start Localtunnel after 2 seconds to make sure server is up
setTimeout(async () => {
    try {
        console.log('🌐 Opening secure tunnel to public internet...');
        const tunnel = await localtunnel({ port: PORT, subdomain: process.env.TUNNEL_SUBDOMAIN || 'jawab-demo' });

        console.log(`\n======================================================`);
        console.log(`✅ JAWAB IS LIVE ON THE PUBLIC INTERNET`);
        console.log(`======================================================`);
        console.log(`Copy and paste these exact URLs into your Twilio Console:`);
        console.log(`\n📞 Call Webhook : ${tunnel.url}/webhook/call`);
        console.log(`💬 WhatsApp Webhook: ${tunnel.url}/webhook/whatsapp`);
        console.log(`\n(Keep this terminal window open during your demo or outreach)`);
        console.log(`======================================================\n`);

        tunnel.on('close', () => {
            console.log('Tunnel closed');
            serverProcess.kill();
        });
    } catch (err) {
        console.error('Failed to start tunnel:', err);
    }
}, 2000);

// Cleanup
process.on('SIGINT', () => {
    console.log('Shutting down...');
    serverProcess.kill();
    process.exit();
});
