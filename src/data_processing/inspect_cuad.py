import json
import os

DATASET_PATH = "data/raw"

print("=" * 60)
print("CUAD DATASET")
print("=" * 60)

print("\nFiles in CUAD folder:")
print("-" * 60)

for item in os.listdir(DATASET_PATH):
    print(item)


# Find CUAD JSON
json_file = os.path.join(
    DATASET_PATH,
    "CUAD_v1.json"
)

print("\n" + "=" * 60)
print("Reading CUAD_v1.json")
print("=" * 60)

with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

print("\nData type:")
print(type(data))

print("\nTop-level information:")

if isinstance(data, dict):

    for key in data.keys():
        print("-", key)

elif isinstance(data, list):

    print("Number of records:", len(data))

print("\nCUAD file loaded successfully!")