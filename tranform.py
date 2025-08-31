import pandas as pd
from pathlib import Path

folder= Path("data")

csv_files = list(folder.glob("*.csv"))

dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    df= df[df["product"]== "pink morsel"]
    df['sales']= df['quantity'] * df['price']
    df= df[['sales', 'date', 'region']]
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)
final_df.to_csv("formatted_sales.csv", index=False)

print("done")

