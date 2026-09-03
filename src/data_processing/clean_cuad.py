import pandas as pd
import os


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

INPUT_FILE = "data/processed/cuad_annotations.csv"

OUTPUT_FILE = "data/processed/cuad_clean.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("=" * 60)
print("LOADING CUAD ANNOTATIONS")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print("\nOriginal number of records:")
print(len(df))


# --------------------------------------------------
# CHECK MISSING VALUES
# --------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())


# --------------------------------------------------
# REMOVE EMPTY TEXT
# --------------------------------------------------

df["text"] = df["text"].fillna("")

df = df[
    df["text"].str.strip() != ""
].copy()

print("\nRecords after removing empty annotations:")
print(len(df))


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=[
        "contract",
        "category",
        "text"
    ]
)

after = len(df)

print("\nDuplicates removed:")
print(before - after)

print("\nRecords after removing duplicates:")
print(after)


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

df["text"] = (
    df["text"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# --------------------------------------------------
# CHECK CATEGORIES
# --------------------------------------------------

print("\nNumber of categories:")
print(df["category"].nunique())

print("\nCategories:")

for i, category in enumerate(
    sorted(df["category"].unique()),
    start=1
):
    print(f"{i:02d}. {category}")


# --------------------------------------------------
# CATEGORY DISTRIBUTION
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORY DISTRIBUTION")
print("=" * 60)

category_counts = (
    df["category"]
    .value_counts()
)

print(category_counts)


# --------------------------------------------------
# SAVE CLEAN DATASET
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
print("CLEAN DATASET SAVED")
print("=" * 60)

print(OUTPUT_FILE)
print("\nFinal number of records:")
print(len(df))