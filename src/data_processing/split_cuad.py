import pandas as pd
from sklearn.model_selection import train_test_split
import os


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

INPUT_FILE = "data/processed/cuad_clean.csv"

TRAIN_FILE = "data/processed/train.csv"
VAL_FILE = "data/processed/validation.csv"
TEST_FILE = "data/processed/test.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("=" * 60)
print("LOADING CLEAN CUAD DATA")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print("\nTotal records:", len(df))

print("Total contracts:", df["contract"].nunique())

print("Total categories:", df["category"].nunique())


# --------------------------------------------------
# GET UNIQUE CONTRACTS
# --------------------------------------------------

contracts = df["contract"].unique().tolist()

print("\nUnique contracts:", len(contracts))


# --------------------------------------------------
# FIRST SPLIT
# 80% TRAIN
# 20% TEMPORARY
# --------------------------------------------------

train_contracts, temp_contracts = train_test_split(
    contracts,
    test_size=0.20,
    random_state=42
)


# --------------------------------------------------
# SECOND SPLIT
# 10% VALIDATION
# 10% TEST
# --------------------------------------------------

val_contracts, test_contracts = train_test_split(
    temp_contracts,
    test_size=0.50,
    random_state=42
)


# --------------------------------------------------
# CREATE DATASETS
# --------------------------------------------------

train_df = df[
    df["contract"].isin(train_contracts)
].copy()

val_df = df[
    df["contract"].isin(val_contracts)
].copy()

test_df = df[
    df["contract"].isin(test_contracts)
].copy()


# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATASET SPLIT")
print("=" * 60)

print("\nTraining:")
print("Contracts:", train_df["contract"].nunique())
print("Records :", len(train_df))

print("\nValidation:")
print("Contracts:", val_df["contract"].nunique())
print("Records :", len(val_df))

print("\nTesting:")
print("Contracts:", test_df["contract"].nunique())
print("Records :", len(test_df))


# --------------------------------------------------
# CHECK FOR OVERLAPPING CONTRACTS
# --------------------------------------------------

train_set = set(train_df["contract"])
val_set = set(val_df["contract"])
test_set = set(test_df["contract"])


print("\n" + "=" * 60)
print("CHECKING CONTRACT OVERLAP")
print("=" * 60)

print(
    "Train ∩ Validation:",
    len(train_set & val_set)
)

print(
    "Train ∩ Test:",
    len(train_set & test_set)
)

print(
    "Validation ∩ Test:",
    len(val_set & test_set)
)


# --------------------------------------------------
# SAVE DATASETS
# --------------------------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)

train_df.to_csv(
    TRAIN_FILE,
    index=False
)

val_df.to_csv(
    VAL_FILE,
    index=False
)

test_df.to_csv(
    TEST_FILE,
    index=False
)


print("\n" + "=" * 60)
print("FILES SAVED")
print("=" * 60)

print(TRAIN_FILE)
print(VAL_FILE)
print(TEST_FILE)