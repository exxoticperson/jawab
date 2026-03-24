// Expanded mapping of Gulf Khaleeji vs English
// This ensures perfect tone without heavy dependencies for the lean MVP.

const getLocalizedResponse = (intent, isEnglish = false) => {
    const responses = {
        greeting: {
            khaleeji: "سوري ما قدرنا نرد عليك! شلون أقدر أساعدك؟",
            en: "Sorry we missed your call! How can I help you today?"
        },
        askName: {
            khaleeji: "ممكن الاسم الكريم؟",
            en: "May I have your name, please?"
        },
        askIssue: {
            khaleeji: "حياك الله. تبي تحجز لشنو بالضبط؟ (فحص، تنظيف، ألم...)",
            en: "Thanks! What would you like to book for? (checkup, cleaning, pain...)"
        },
        provideLink: {
            khaleeji: "تمام، تقدر تختار الوقت اللي يناسبك من هذا الرابط: ",
            en: "Perfect, you can pick a time that works for you here: "
        },
        handoff: {
            khaleeji: "دقيقة وأبلغ الفريق بالعيادة يتواصلون معاك الحين.",
            en: "One moment, I'll notify the clinic team right now to assist you."
        },
        alreadyHandled: {
            khaleeji: "تم التبليغ وتقدر تتواصل مع الفريق مباشرة. محتاج شي ثاني الحين؟",
            en: "The team has been notified. Do you need anything else right now?"
        }
    };
    
    return isEnglish ? responses[intent].en : responses[intent].khaleeji;
};

// Very simple heuristic to detect English characters vs Arabic
const isEnglishText = (text) => {
    // If more than 50% of the letters are a-z, consider it English or Arabizi
    const engMatches = text.match(/[a-zA-Z]/g);
    const engCount = engMatches ? engMatches.length : 0;
    return engCount >= (text.length / 2);
};

module.exports = { getLocalizedResponse, isEnglishText };
