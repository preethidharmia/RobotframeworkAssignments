# Create a New Column Based on Conditions Use np.
# where() or apply() to classify rows as:
# "High Salary" if salary > 75,000 "Medium Salary" if salary between 40,000-75,000 "Low Salary" otherwise

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["A", "B", "C", "D"],
    "salary": [90000, 50000, 30000, 75000]
})

df["salary_level"] = np.where(df["salary"] > 75000, "High Salary",
                              np.where(df["salary"] >= 40000, "Medium Salary",
                                       "Low Salary"))

print(df)
