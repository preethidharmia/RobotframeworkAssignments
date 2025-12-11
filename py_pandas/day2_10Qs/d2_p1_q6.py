# Convert Wide Format Data to Long Format Using melt(),
# convert a DataFrame of student marks across subjects into a long-form structure with
# columns: student, subject, marks.

import pandas as pd

df = pd.DataFrame({
    "student": ["John", "Mary"],
    "math": [80, 90],
    "science": [85, 95],
    "english": [78, 88]
})

long_df = df.melt(id_vars="student",
                  var_name="subject",
                  value_name="marks")

print(long_df)
