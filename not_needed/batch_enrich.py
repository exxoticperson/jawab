import csv
import json

# This is a helper script to structure the enrichment data
# I will fill the actual data from the search tool results

input_file = "/home/ubuntu/high_potential_leads.csv"
output_file = "/home/ubuntu/enriched_leads.csv"

# I'll process the first 20 for now to demonstrate the flow and conserve credits
# and then I can do more if needed.

fieldnames = ["Clinic Name", "City", "Website", "Instagram", "Google Rating", "Review Count"]

with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

print("Enrichment file initialized.")
