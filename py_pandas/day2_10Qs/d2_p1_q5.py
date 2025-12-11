# Calculate Rolling Window Statistics, Given time-series stock prices,
# compute a 7-day rolling mean and 14-day rolling standard deviation.

import pandas as pd

df = pd.DataFrame({
    "date": pd.date_range(start="2024-01-01", periods=20, freq="D"),
    "price": [i*2 for i in range(20)]
})

df.set_index("date", inplace=True)

df["rolling_mean_7"] = df["price"].rolling(7).mean()
df["rolling_std_14"] = df["price"].rolling(14).std()

print(df)
