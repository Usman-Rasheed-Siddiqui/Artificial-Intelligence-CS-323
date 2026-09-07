import numpy as np
import pandas as pd

from sklearn.preprocessing import (
    MinMaxScaler,
    StandardScaler,
    OrdinalEncoder
)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("Lab/coffee_small.csv")


# ==========================================
# TAKE ONLY FIRST 10 ROWS
# ==========================================

df = df.head(10).copy()


print("==========================================")
print("ORIGINAL FIRST 10 ROWS")
print("==========================================")

print(df)


# ==========================================
# DATA CLEANING
# ==========================================

# Convert estimated price into numeric
#
# "$50.00/4 ounces"  -> 50.00
# "$26.00/8 ounces"  -> 26.00
# "NT $450/8 ounces" -> 450.00

df["est_price"] = (
    df["est_price"]
    .astype(str)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

df["est_price"] = pd.to_numeric(
    df["est_price"],
    errors="coerce"
)


# Fill missing numerical values with median

numeric_columns = [
    "aroma",
    "body",
    "flavor",
    "est_price"
]

for column in numeric_columns:
    df[column] = df[column].fillna(
        df[column].median()
    )


# Fill missing categorical values

df["roast_level"] = df["roast_level"].fillna("Medium")
df["origin"] = df["origin"].fillna("Unknown")


# ==========================================
# SEPARATE INPUTS AND OUTPUT
# ==========================================

# Input parameters
X = df[
    [
        "aroma",
        "body",
        "flavor",
        "roast_level",
        "origin",
        "est_price"
    ]
].copy()


# Output / Target
Y = df["rating"].copy()


# ==========================================
# 1. NORMALIZATION
# ==========================================
# Feature: aroma
# Min-Max Normalization
# Range: 0 to 1

normalizer = MinMaxScaler()

X["aroma_Normalized"] = normalizer.fit_transform(
    X[["aroma"]]
).flatten()


# ==========================================
# 2. STANDARDIZATION
# ==========================================
# Feature: body
# Z-score Standardization

standardizer = StandardScaler()

X["body_Standardized"] = standardizer.fit_transform(
    X[["body"]]
).flatten()


# ==========================================
# 3. SCALING
# ==========================================
# Feature: est_price
# Min-Max Scaling
# Range: 0 to 1

scaler = MinMaxScaler()

X["est_price_Scaled"] = scaler.fit_transform(
    X[["est_price"]]
).flatten()


# ==========================================
# 4. ORDINAL ENCODING
# ==========================================
# Feature: roast_level
#
# Light < Medium-Light < Medium
# < Medium-Dark < Dark < Very Dark

roast_order = [
    "Light",
    "Medium-Light",
    "Medium",
    "Medium-Dark",
    "Dark",
    "Very Dark"
]

ordinal_encoder = OrdinalEncoder(
    categories=[roast_order],
    handle_unknown="use_encoded_value",
    unknown_value=-1
)

X["roast_level_Ordinal"] = ordinal_encoder.fit_transform(
    X[["roast_level"]]
).flatten()


# ==========================================
# 5. ONE-HOT ENCODING
# ==========================================
# Feature: origin

X = pd.get_dummies(
    X,
    columns=["origin"],
    prefix="origin",
    dtype=int
)


# ==========================================
# 6. BINNING
# ==========================================
# Feature: flavor
#
# 0 - 7   = Low
# 7 - 8   = Good
# 8 - 9   = Excellent
# 9 - 10  = Outstanding

flavor_bins = [
    0,
    7,
    8,
    9,
    10
]

flavor_labels = [
    "Low",
    "Good",
    "Excellent",
    "Outstanding"
]

X["flavor_Binned"] = pd.cut(
    X["flavor"],
    bins=flavor_bins,
    labels=flavor_labels,
    include_lowest=True
)


# ==========================================
# ADD OUTPUT / TARGET
# ==========================================

X["rating"] = Y.values


# ==========================================
# FINAL PREPROCESSED TABLE
# ==========================================

print("\n==========================================")
print("FINAL PREPROCESSED FIRST 10 ROWS")
print("==========================================")

print(X)


# ==========================================
# SAVE RESULT
# ==========================================

X.to_csv(
    "Lab/coffee_preprocessed.csv",
    index=False
)

print("\n==========================================")
print("SUCCESS")
print("==========================================")

print("Only the first 10 rows were preprocessed.")
print("Saved as: Lab/coffee_preprocessed.csv")