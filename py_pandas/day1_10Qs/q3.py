import pandas as pd

df = pd.read_csv("employees.csv")
avg_salary = df.groupby("department")["salary"].mean()
print(avg_salary)
#Write a program to group employees by department and calculate average salary.