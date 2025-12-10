import pandas as pd

df = pd.read_csv("ts.csv", parse_dates=["date"])

weekly = df.groupby(pd.Grouper(key="date", freq="W"))["value"].sum()
print(weekly)

#Given a time-series DataFrame, resample it into weekly summaries.