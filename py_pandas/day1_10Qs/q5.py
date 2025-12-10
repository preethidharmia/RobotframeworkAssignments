import pandas as pd

df = pd.read_csv("sales_data.csv")
pt = df.pivot_table(values="sales", index="month", columns="region", aggfunc="sum")
print(pt)

#Create a pivot table to show sales per month per region.