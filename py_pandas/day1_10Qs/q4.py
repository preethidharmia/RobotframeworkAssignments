import pandas as pd

emp = pd.read_csv("emp.csv")
sal = pd.read_csv("salary.csv")

merged = pd.merge(emp, sal, on="emp_id")
print(merged)

#Merge two DataFrames (employee details and salary detais) using merge().