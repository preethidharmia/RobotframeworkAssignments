# Filter Rows Based on Text Pattern Using str.contains(),
# filter all rows where a column (e.g., "comments") contains the keyword "refund".

import pandas as pd

df = pd.DataFrame({
    "comments": [
        "Customer requested refund",
        "Payment received",
        "REFUND processed",
        "No action needed"
    ]
})

refund_rows = df[df["comments"].str.contains("refund", case=False, na=False)]

print(refund_rows)
