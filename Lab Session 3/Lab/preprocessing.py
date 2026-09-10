
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler, StandardScaler, OrdinalEncoder

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("Lab/coffee.csv")

print("Original Dataset:")
print(df.head(10))

print("\nDataset Information:")
print(df.info())

print("\nShape:")
print(df.shape)


# ==========================================
# DATA CLEANING
# ==========================================

# Convert agtron to numeric
df["agtron"] = pd.to_numeric(df["agtron"], errors="coerce")

# Convert price to numeric
df["est_price"] = (
    df["est_price"]
    .astype(str)
    .str.replace(r"[^0-9.]", "", regex=True)
)

df["est_price"] = pd.to_numeric(
    df["est_price"],
    errors="coerce"
)

sample = df.copy()

# ==========================================
# NORMALIZATION
# ==========================================

normalizer = MinMaxScaler()

sample["rating_Normalized"] = normalizer.fit_transform(
    sample[["rating"]].fillna(sample["rating"].median())
).flatten()

# ==========================================
# STANDARDIZATION
# ==========================================

standardizer = StandardScaler()

sample["aroma_Standardized"] = standardizer.fit_transform(
    sample[["aroma"]].fillna(sample["aroma"].median())
).flatten()

# ==========================================
# SCALING
# ==========================================

scaler = MinMaxScaler()

sample["body_Scaled"] = scaler.fit_transform(
    sample[["body"]].fillna(sample["body"].median())
).flatten()

# ==========================================
# ORDINAL ENCODING
# ==========================================

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

sample["roast_level_Ordinal"] = ordinal_encoder.fit_transform(
    sample[["roast_level"]].fillna("Medium")
).flatten()

print("\nAfter Ordinal Encoding:")
print(
    sample[
        ["roast_level", "roast_level_Ordinal"]
    ]
)

# ==========================================
# ONE-HOT ENCODING
# ==========================================

sample = pd.get_dummies(
    sample,
    columns=["origin"],
    prefix="origin",
    dtype=int
)

# ==========================================
# BINNING
# ==========================================

bins = [0, 84, 89, 94, 100]

labels = [
    "Average",
    "Good",
    "Excellent",
    "Outstanding"
]

sample["rating_Binned"] = pd.cut(
    sample["rating"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# ==========================================
# FINAL PREPROCESSED TABLE
# ==========================================

print("\n==========================================")
print("FINAL PREPROCESSED DATA")
print("==========================================")

print(sample.head(10))

sample.to_csv(
    "Lab/coffee_preprocessed.csv",
    index=False
)

print("\nPreprocessed dataset saved successfully!")

