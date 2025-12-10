import pandas as pd

df = pd.read_csv("dups.csv")
clean = df.drop_duplicates()
print(clean)

#write a program to remove duplicate rows from a DataFrame.