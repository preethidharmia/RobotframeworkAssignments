import pandas as pd

df = pd.read_csv("students.csv")
print("Column Names:", df.columns.tolist())
print(df.head(10))

# var = (df := pd.read_csv("students.csv")
#        .pipe(lambda d: (print("Cols:", list(d)), d)[1])
#        .pipe(lambda d: (print(d.head(10)), d)[1])
#        )


#load a CSV file and display the first 10 rows along with column names.