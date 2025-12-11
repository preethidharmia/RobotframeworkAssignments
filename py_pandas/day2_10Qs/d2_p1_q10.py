# Detect Duplicate Records Based on Selected Columns.

import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "A", "C"],
    "age": [25, 30, 25, 40]
})

duplicates = df[df.duplicated(subset=["name", "age"], keep=False)]

print(duplicates)
