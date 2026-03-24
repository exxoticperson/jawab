import csv

keywords = [
    "cosmetic", "implant", "specialized", "laser", "german", "american", 
    "british", "canadian", "french", "aesthetic", "orthodontic", "studio", 
    "smile", "luxe", "premium", "advanced", "center", "centre", "modern"
]

input_file = "/home/ubuntu/all_leads_raw.csv"
output_file = "/home/ubuntu/high_potential_leads.csv"

high_potential = []

with open(input_file, mode='r', encoding='utf-8') as infile:
    # Use DictReader with robust handling
    reader = csv.DictReader(infile)
    for row in reader:
        # Filter out rows that might have extra columns or parsing issues
        if None in row:
            del row[None]
            
        name = (row.get('Clinic Name') or "").lower()
        services = (row.get('Products & Services') or "").lower()
        
        # Check if any keyword is in the name or services
        if any(kw in name for kw in keywords) or any(kw in services for kw in keywords):
            high_potential.append(row)

# Save filtered list
if high_potential:
    # Ensure all rows have the same keys
    fieldnames = ["Clinic Name", "Location", "City", "Phone", "Products & Services"]
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(high_potential)

print(f"Filtered {len(high_potential)} high-potential leads from the original list.")
