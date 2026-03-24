#!/usr/bin/env python3
import csv
import sys
import argparse
import re

# Bilingual keywords for pain signals
PAIN_KEYWORDS = [
    # English
    r"couldn't reach", r"no answer", r"didn't call back", r"hard to book", 
    r"waited long time", r"receptionist", r"phone", r"whatsapp", r"unresponsive",
    r"no reply", r"calling", r"nobody picks up", r"ignored",
    # Arabic
    r"ما قدرت أتواصل", r"ما حد رد", r"ما اتصلوا", r"صعب الحجز", 
    r"انتظرت وايد", r"ريسبشن", r"تلفون", r"واتساب", r"محد يرد",
    r"استقبال سيء", r"تأخير", r"ما يردون"
]

def analyze_reviews(input_file, output_file):
    """
    Reads a CSV containing clinic reviews, scans for pain signals,
    and outputs the enriched data.
    Note: This is a simulation script. In a real scenario, it would take
    review text as input. For this skill, we assume the input CSV has a 'Review Text' column.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            if not fieldnames:
                print("Error: Input file is empty or has no headers.")
                return

            # Add new fields if they don't exist
            new_fields = ['Pain Signal Found', 'Pain Signal Type', 'Exact Review Quote']
            for field in new_fields:
                if field not in fieldnames:
                    fieldnames.append(field)

            rows = list(reader)

            for row in rows:
                review_text = row.get('Review Text', '').lower()
                pain_found = False
                matched_quote = ""
                pain_type = "None"

                if review_text:
                    for keyword in PAIN_KEYWORDS:
                        if re.search(keyword, review_text, re.IGNORECASE):
                            pain_found = True
                            # Simple extraction: get the sentence containing the keyword
                            sentences = re.split(r'[.!?\n]', review_text)
                            for sentence in sentences:
                                if re.search(keyword, sentence, re.IGNORECASE):
                                    matched_quote = sentence.strip()
                                    break
                            
                            # Categorize type
                            if any(k in keyword for k in ['phone', 'call', 'reach', 'تلفون', 'اتصل', 'تواصل']):
                                pain_type = 'phone'
                            elif any(k in keyword for k in ['book', 'حجز']):
                                pain_type = 'booking'
                            elif any(k in keyword for k in ['reception', 'ريسبشن', 'استقبال']):
                                pain_type = 'front desk'
                            else:
                                pain_type = 'response'
                            break # Stop after first match

                row['Pain Signal Found'] = 'Yes' if pain_found else 'No'
                row['Pain Signal Type'] = pain_type if pain_found else 'Not found'
                row['Exact Review Quote'] = matched_quote if pain_found else 'Not found'

            # Write output
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Successfully analyzed reviews for {len(rows)} clinics. Output saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract pain signals from clinic reviews.")
    parser.add_argument("input_csv", help="Path to input CSV file containing 'Review Text'")
    parser.add_argument("output_csv", help="Path to output CSV file")
    args = parser.parse_args()
    
    analyze_reviews(args.input_csv, args.output_csv)
