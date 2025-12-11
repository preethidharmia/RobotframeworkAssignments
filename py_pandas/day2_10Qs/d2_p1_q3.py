# Create a MultiIndex DataFrame, Create a MultiIndex DataFrame using two categorical columns
# (eg., Region and Product) and apply an aggregation such as total sales.

import pandas as pd

df = pd.DataFrame({
    "Region": ["East", "East", "West", "West"],
    "Product": ["A", "B", "A", "B"],
    "Sales": [1200, 1500, 1700, 1600],
    "Sales_thru": ["Amazon", "Flipkart", "Flipkart", "Amazon"]
})
result = df.groupby(["Region", "Product", "Sales_thru"]).agg(total_sales=("Sales", "sum"))
print(result)
