import csv
import json
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    data = list(reader)

with open(output_file, mode='w', encoding='utf-8') as outfile:
    json.dump(data, outfile)
