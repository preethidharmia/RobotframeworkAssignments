# Rank Employees Based on Performance,Given a DataFrame of employees with performance scores,
# use rank() to assign ranks in descending order and handle ties properly.

import pandas as pd

df = pd.DataFrame({
    "employee": ["Aswatha", "Bhairavi", "Chandini", "Deeksha", "Esha", "Farjana"],
    "performance_stars": [4.5, 3.5, 4.0, 4.6, 4.5, 4.0]
})
df["rank"] = df["performance_stars"].rank(method="dense", ascending=False)
df["rank"] = df["rank"].astype(int)
print(df)
