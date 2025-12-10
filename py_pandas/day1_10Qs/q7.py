import pandas as pd

df = pd.read_csv("products.csv")
df_dummies = pd.get_dummies(df, columns=["category"])
print(df_dummies)

#Convert a column with categorical values into dummy variables using get_dummies().