import pandas as pd

df = pd.read_csv("sales.csv")
df_filled = df.fillna(df.mean(numeric_only=True))
print(df_filled)

#Given a DataFrame, fill missing values using the mean of the respective column.