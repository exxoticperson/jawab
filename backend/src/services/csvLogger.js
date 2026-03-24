const fs = require('fs');
const path = require('path');
const { createObjectCsvWriter } = require('csv-writer');

/**
 * Standardized logging pushes data to a local CSV file (acting as the Google Sheet logic)
 * so the founder has an instant, tangible report to show clinics without configuring webhooks.
 */
const logConversation = async (clinicId, patientNumber, language, outcome) => {
    try {
        const filePath = path.join(__dirname, '..', '..', 'reports', `${clinicId}_recovered.csv`);
        const reportDir = path.join(__dirname, '..', '..', 'reports');
        
        // Ensure reports directory exists
        if (!fs.existsSync(reportDir)){
            fs.mkdirSync(reportDir);
        }

        const csvWriter = createObjectCsvWriter({
            path: filePath,
            header: [
                {id: 'timestamp', title: 'Timestamp'},
                {id: 'clinicId', title: 'Clinic ID'},
                {id: 'patientNumber', title: 'Patient Number'},
                {id: 'language', title: 'Language'},
                {id: 'outcome', title: 'Outcome'}
            ],
            append: fs.existsSync(filePath) // Only append headers if file is new
        });

        const payload = {
            timestamp: new Date().toISOString(),
            clinicId,
            patientNumber: patientNumber.slice(-4), // Hash full number for privacy V1
            language,
            outcome
        };
        
        await csvWriter.writeRecords([payload]);
        console.log(`[LOG] Successfully wrote recovery record to ${filePath}`);

    } catch (error) {
        console.error('[ERROR] Failed to write CSV', error.message);
    }
};

module.exports = { logConversation };
