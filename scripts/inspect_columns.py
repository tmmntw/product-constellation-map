import pandas as pd

df = pd.read_csv("strategy_matrix.csv")
print("COLUMNS:")
for c in df.columns:
    print("-", c)
