#!/usr/bin/env python3
import csv
import sys
import argparse

def score_clinics(input_file, output_file):
    """
    Reads clinic data from a CSV, calculates the ICP score (0-3),
    determines the tier (A, B, C), and writes the enriched data to a new CSV.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            if not fieldnames:
                print("Error: Input file is empty or has no headers.")
                return

            # Add new fields if they don't exist
            if 'ICP Score' not in fieldnames:
                fieldnames.append('ICP Score')
            if 'Tier' not in fieldnames:
                fieldnames.append('Tier')

            rows = list(reader)

            for row in rows:
                score = 0
                
                # 1. Specialty match (cosmetic, implant, or aesthetic = 1 point)
                specialty = row.get('Specialty', '').lower()
                if any(kw in specialty for kw in ['cosmetic', 'implant', 'aesthetic']):
                    score += 1

                # 2. Digital presence (Instagram active AND website = 1 point)
                has_ig = row.get('Instagram Handle', '').strip() not in ['', 'Not found']
                has_website = row.get('Website', '').strip() not in ['', 'Not found']
                if has_ig and has_website:
                    score += 1

                # 3. Pain signal found (at least one review with phone/booking complaint = 1 point)
                pain_signal = row.get('Pain Signal Found', '').lower()
                if pain_signal in ['yes', 'true', '1']:
                    score += 1

                row['ICP Score'] = score

                # Determine Tier
                review_count_str = row.get('Google Review Count', '0')
                try:
                    review_count = int(''.join(filter(str.isdigit, review_count_str)))
                except ValueError:
                    review_count = 0

                if score == 3 or (score == 2 and review_count >= 100):
                    row['Tier'] = 'A'
                elif score == 2:
                    row['Tier'] = 'B'
                else:
                    row['Tier'] = 'C'

            # Sort: First by ICP Score (desc), then by Review Count (desc)
            def sort_key(r):
                score = int(r.get('ICP Score', 0))
                try:
                    reviews = int(''.join(filter(str.isdigit, r.get('Google Review Count', '0'))))
                except ValueError:
                    reviews = 0
                return (score, reviews)

            rows.sort(key=sort_key, reverse=True)

            # Write output
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Successfully scored and tiered {len(rows)} clinics. Output saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score and tier Jawab clinic leads.")
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_csv", help="Path to output CSV file")
    args = parser.parse_args()
    
    score_clinics(args.input_csv, args.output_csv)
