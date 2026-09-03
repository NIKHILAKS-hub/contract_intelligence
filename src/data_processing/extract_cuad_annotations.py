import json
import pandas as pd
import os
import re

# --------------------------------------------------
# PATHS
# --------------------------------------------------

INPUT_FILE = "data/raw/CUAD_v1.json"

OUTPUT_FILE = "data/processed/cuad_annotations.csv"


# --------------------------------------------------
# LOAD CUAD
# --------------------------------------------------

print("=" * 60)
print("LOADING CUAD DATASET")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    cuad = json.load(file)

contracts = cuad["data"]

print("Number of contracts:", len(contracts))


# --------------------------------------------------
# EXTRACT ANNOTATIONS
# --------------------------------------------------

records = []

for contract in contracts:

    contract_title = contract["title"]

    for paragraph in contract["paragraphs"]:

        context = paragraph["context"]

        for qa in paragraph["qas"]:

            question = qa["question"]

            # --------------------------------------------------
            # Extract category name from question
            # --------------------------------------------------

            match = re.search(
                r'related to "([^"]+)"',
                question
            )

            if match:
                category = match.group(1)
            else:
                category = question

            # --------------------------------------------------
            # Get answers
            # --------------------------------------------------

            answers = qa.get("answers", [])

            if len(answers) == 0:

                records.append({
                    "contract": contract_title,
                    "category": category,
                    "text": "",
                    "answer_start": None
                })

            else:

                for answer in answers:

                    records.append({
                        "contract": contract_title,
                        "category": category,
                        "text": answer["text"],
                        "answer_start": answer["answer_start"]
                    })


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(records)


# --------------------------------------------------
# DISPLAY INFORMATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("EXTRACTION COMPLETE")
print("=" * 60)

print("\nTotal annotation records:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 records:")
print(df.head(10).to_string(index=False))


# --------------------------------------------------
# SHOW CATEGORIES
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUAD CATEGORIES")
print("=" * 60)

categories = sorted(
    df["category"].unique()
)

print("\nNumber of unique categories:")
print(len(categories))

for number, category in enumerate(categories, start=1):

    print(f"{number:02d}. {category}")


# --------------------------------------------------
# SAVE
# --------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\n" + "=" * 60)
print("FILE SAVED")
print("=" * 60)

print(OUTPUT_FILE)