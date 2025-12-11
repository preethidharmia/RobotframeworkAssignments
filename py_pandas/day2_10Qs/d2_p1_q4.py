# Sort a DataFrame by Multiple Columns Sort a DataFrame first by "department",
# then by "salary" in decreasing order.

import pandas as pd

df = pd.DataFrame({
    "department": ["HR", "Finance", "HR", "IT", "HR", "IT", "Admin", "IFM"],
    "salary": [50000, 70000, 65000, 90000, 45000, 93000, 65000, 30000]
})
sorted_df = df.sort_values(by=["department", "salary"], ascending=[True, False])
print(sorted_df)
