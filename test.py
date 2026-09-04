import pandas as pd
df = pd.read_parquet("data/depth_1788537279.parquet")
print(df.columns.tolist())
print(df.head())
