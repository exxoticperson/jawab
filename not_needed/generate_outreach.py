import csv

def generate_whatsapp_message(clinic_name, google_rating, review_count, city):
    # Personalized angle based on available data (Google Rating and Review Count)
    # Since pain signals were not extracted, we'll use a general approach.
    personalized_angle = f"عيادتكم {clinic_name} في {city} لها تقييم {google_rating} مع أكثر من {review_count} مراجعة، وهذا يدل على حجم عمل كبير. "
    
    # Example of a personalized angle if we had pain signals:
    # personalized_angle = f"شفت ريفيوهات المرضى يذكرون صعوبة التواصل بالتلفون في عيادتكم {clinic_name}. "

    message = f"د. {clinic_name} — {personalized_angle} أنا طبيب أسنان وعندي خبرة بخدمة العملاء. بنيت نظام اسمه جواب — يمسك كل مكالمة فايتة ويتواصل مع المريض بالواتساب فوراً — عربي وإنجليزي. عندي عرض سريع ٦٠ ثانية. تبي تشوفه؟"
    return message

input_file = "/home/ubuntu/scored_leads.csv"
output_file = "/home/ubuntu/outreach_messages.csv"

outreach_messages = []

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if row["Tier"] == "A":
            clinic_name = row["Clinic Name"]
            google_rating = row["Google Rating"]
            review_count = row["Review Count"]
            city = row["City"]
            whatsapp_message = generate_whatsapp_message(clinic_name, google_rating, review_count, city)
            outreach_messages.append({
                "Clinic Name": clinic_name,
                "Tier": "A",
                "Outreach Channel": "WhatsApp",
                "Message": whatsapp_message
            })

if outreach_messages:
    fieldnames = ["Clinic Name", "Tier", "Outreach Channel", "Message"]
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(outreach_messages)

print(f"Generated {len(outreach_messages)} personalized outreach messages for Tier A clinics.")
