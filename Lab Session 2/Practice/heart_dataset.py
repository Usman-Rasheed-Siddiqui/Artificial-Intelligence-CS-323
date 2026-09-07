
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Load your dataset (update the filename if necessary)
df = pd.read_csv('Heart_Dataset.csv')

# View the first 5 rows to inspect structure
print(df.head())

# Check total rows, columns, and data types
print(df.info())

# Separate features and target
X = df.drop(columns=['HeartDisease'])
Y = df['HeartDisease']

# One-hot encode string columns
X_encoded = pd.get_dummies(X, drop_first=True)

# View new structure and columns
print("New encoded shape:", X_encoded.shape)
print(X_encoded.head())


X_train, X_test, Y_train, Y_test = train_test_split(
    X_encoded, Y, test_size=0.20, random_state=42, stratify=Y
)

print(f"Training set: {X_train.shape}")
print(f"Testing set: {X_test.shape}")

scaler = MinMaxScaler()

# Fit on training data ONLY, then transform both train and test
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrame to view statistics
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_encoded.columns)

print("\n--- Min-Max Scaled Data Summary ---")
print(X_train_scaled_df.describe().loc[['min', 'max']])
