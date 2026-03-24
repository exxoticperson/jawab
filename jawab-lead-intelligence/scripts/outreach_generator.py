#!/usr/bin/env python3
import csv
import sys
import argparse

def generate_outreach(input_file, output_file):
    """
    Reads Tier A clinics and generates personalized outreach drafts.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            if not fieldnames:
                print("Error: Input file is empty or has no headers.")
                return

            new_fields = ['Personalized Angle (AR)', 'Personalized Angle (EN)', 'WhatsApp Draft (AR)', 'Instagram Draft (EN)', 'Email Draft (EN)']
            for field in new_fields:
                if field not in fieldnames:
                    fieldnames.append(field)

            rows = list(reader)

            for row in rows:
                if row.get('Tier', '') != 'A':
                    continue # Only process Tier A

                name = row.get('Owner/Lead Dentist Name', 'Doctor')
                if name in ['', 'Not found']:
                    name = 'Doctor'
                
                clinic_name = row.get('Clinic Name', 'Your Clinic')
                pain_quote = row.get('Exact Review Quote', '')
                has_ig = row.get('Instagram Handle', '').strip() not in ['', 'Not found']
                has_wa = row.get('WhatsApp Number', '').strip() not in ['', 'Not found', 'Not visible']

                # Generate Angle
                angle_ar = ""
                angle_en = ""
                
                if pain_quote and pain_quote != 'Not found':
                    angle_ar = "شفت ريفيوهات المرضى يذكرون صعوبة التواصل بالتلفون"
                    angle_en = "Your Google reviews show patients love your work, but several mention difficulty reaching you by phone"
                elif has_ig and not has_wa:
                    angle_ar = "شفت شغلكم الجميل بالإنستغرام بس ما حصلت رقم واتساب للتواصل"
                    angle_en = "Your Instagram shows beautiful cases, but I couldn't find a WhatsApp number on your site"
                else:
                    angle_ar = "اتصلت على الرقم الموجود بقوقل وما أحد رد بعد ٣٠ ثانية"
                    angle_en = "I tried calling your number from your Google listing and it rang out after 30 seconds"

                row['Personalized Angle (AR)'] = angle_ar
                row['Personalized Angle (EN)'] = angle_en

                # Generate WhatsApp (AR)
                wa_draft = f"د. {name} — {angle_ar}.\n\nأنا طبيب أسنان وعندي خبرة بخدمة العملاء. بنيت نظام اسمه جواب — يمسك كل مكالمة فايتة ويتواصل مع المريض بالواتساب فوراً — عربي وإنجليزي.\n\nعندي عرض سريع ٦٠ ثانية. تبي تشوفه؟"
                row['WhatsApp Draft (AR)'] = wa_draft

                # Generate Instagram (EN)
                ig_draft = f"Dr. {name} — {angle_en}. I'm a dentist who built a system called Jawab that catches every missed call and follows up via WhatsApp — Arabic and English. I have a 60-second walkthrough. Want to see it?"
                row['Instagram Draft (EN)'] = ig_draft

                # Generate Email (EN)
                email_draft = f"Subject: Missed calls at {clinic_name}\n\nHi Dr. {name},\n\n{angle_en}.\n\nI'm a dentist with customer service experience and I built Jawab — a bilingual WhatsApp system that recovers missed calls for Gulf dental clinics. I have a 60-second walkthrough showing how it works.\n\nWould it be useful for me to send it?"
                row['Email Draft (EN)'] = email_draft

            # Write output
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Successfully generated outreach for Tier A clinics. Output saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate personalized outreach drafts for Tier A clinics.")
    parser.add_argument("input_csv", help="Path to input CSV file containing Tier A clinics")
    parser.add_argument("output_csv", help="Path to output CSV file")
    args = parser.parse_args()
    
    generate_outreach(args.input_csv, args.output_csv)
