import pandas as pd

# ==========================================
# LOAD ORIGINAL DATASET
# ==========================================

df = pd.read_csv("Lab/coffee.csv")


# ==========================================
# SELECT REQUIRED COLUMNS
# ==========================================

small_df = df[
    [
        "aroma",
        "body",
        "flavor",
        "roast_level",
        "origin",
        "est_price",
        "rating"
    ]
].copy()


# ==========================================
# SAVE REDUCED DATASET
# ==========================================

small_df.to_csv(
    "Lab/coffee_small.csv",
    index=False
)


# ==========================================
# DISPLAY DATASET
# ==========================================

print("==========================================")
print("REDUCED COFFEE DATASET")
print("==========================================")

print(small_df.head(10))

print("\nShape:")
print(small_df.shape)

print("\nData Types:")
print(small_df.dtypes)