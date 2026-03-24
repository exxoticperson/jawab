const fs = require('fs');
const path = require('path');

const loadClinicConfig = (incomingNumber) => {
    try {
        const configPath = path.join(__dirname, 'tenants.json');
        const rawData = fs.readFileSync(configPath, 'utf-8');
        const tenants = JSON.parse(rawData);
        
        // Find tenant by the number they called (the Twilio number pointing to Jawab)
        // Adjust logic if matching against clinic's exact Twilio number format
        let match = tenants.find(t => t.twilioNumber === incomingNumber || incomingNumber.includes(t.twilioNumber));
        
        // Return match or the first demo clinic as default for testing
        return match || tenants[0];
    } catch (e) {
        console.error("Failed to load clinic configs", e.message);
        return null; // Handle properly in controller
    }
};

module.exports = { loadClinicConfig };
