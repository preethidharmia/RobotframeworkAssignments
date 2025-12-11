# Replace Specific Values in a DataFrame Replace all occurrences of "Not Available"
# or "N/A" in a dataset with np.nan.

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "col": ["value1", "N/A", "Not Available", "value4"]
})

df.replace(["N/A", "Not Available"], np.nan, inplace=True)

print(df)
