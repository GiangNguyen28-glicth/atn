import json
import sys
# from tabulate import tabulate
from transformer import Transformer
with open("/Users/giangnt/code/athena/opensanctions/data/hr_crime_opensanctions.jsonl", encoding="utf-8") as f:
    results = []
    for line in f:
        row = json.loads(line)
        info = row["information"]
        if isinstance(info, str):
            try:
                info = json.loads(info)
            except Exception as e:
                print(e)
                continue
        if not isinstance(info, dict):
            print("Data is not dict")
            continue
        
        if "schema" not in info:
            continue
        
        # person = parse_crime_opensanction(info)
        transformer = Transformer()
        properties = info["properties"]
        nested = properties.get("sanctions")
        if nested is not None:
            print(nested)
        entity = transformer.transform(raw_data=row)
        # results.append(entity)
        # table = [[k, str(v)] for k, v in person.items()]
        # print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))

        # sys.exit()
    print(f"Total entities has been transform: {len(results)}")
