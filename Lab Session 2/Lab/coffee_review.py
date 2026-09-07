import pandas as pd
import numpy as np

# Load your dataset (update the filename if necessary)
df = pd.read_csv('Lab/coffee.csv')

# View the first 5 rows to inspect structure
print(df.head())

# Check total rows, columns, and data types
print(df.info())