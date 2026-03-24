import csv

def score_clinic(row):
    score = 0
    # Criteria 1: Premium Keywords in Name/Services (Already filtered, but let's check)
    premium_keywords = ["cosmetic", "implant", "specialized", "laser", "german", "american", "aesthetic", "orthodontic"]
    name = row.get('Clinic Name', '').lower()
    if any(kw in name for kw in premium_keywords):
        score += 1
        
    # Criteria 2: Google Rating >= 4.5
    try:
        rating = float(row.get('Google Rating', 0))
        if rating >= 4.5:
            score += 1
    except ValueError:
        pass
        
    # Criteria 3: Review Count > 100
    try:
        reviews = int(row.get('Review Count', 0))
        if reviews > 100:
            score += 1
    except ValueError:
        pass
        
    # Assign Tier
    if score >= 3:
        tier = "A"
    elif score == 2:
        tier = "B"
    else:
        tier = "C"
        
    return score, tier

input_file = "/home/ubuntu/enriched_leads.csv"
output_file = "/home/ubuntu/scored_leads.csv"

scored_leads = []

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        score, tier = score_clinic(row)
        row['ICP Score'] = score
        row['Tier'] = tier
        scored_leads.append(row)

if scored_leads:
    fieldnames = list(scored_leads[0].keys())
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_leads)

print(f"Scored {len(scored_leads)} leads and assigned tiers.")
