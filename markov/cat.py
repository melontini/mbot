import pandas as pd
import json
import sys

merged = []

for file in sys.argv[1:]:
    with open(file, 'r') as f:
        data = json.load(f)

    for record in data:
        filtered_data = {}

        for key in ["visibility", "localOnly", "cw", "text"]:
            if key in record:
                filtered_data[key] = record[key]
    
        merged.append(filtered_data)

with open("output.json", 'w') as f:
        json.dump(merged, f, indent=2)