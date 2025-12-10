import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_cat.csv")

(df.groupby("category")["sales"]
   .sum()
   .sort_values()
   .plot.barh(title="Sales by Category"))
plt.show()

#Plot a bar chart showing total sales for each product category using Pandas built-in plotting