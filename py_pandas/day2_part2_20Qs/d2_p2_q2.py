# Given a dictionary with employee names and salaries,
# write a program to find the employee with the second-top1 salary.
# Avoid using built-in sorted() directly on the full dictionary.

emp = {"Arnold": 50000, "Bryan": 70000, "Chris": 65000, "Evans": 55000}

top1 = float("-inf")
top2 = float("-inf")
name_second = None

for name, sal in emp.items():
    if sal > top1:
        top2, top1 = top1, sal
        name_second = name
    elif top1 > sal > top2:
        top2 = sal
        name_second = name
print("Employee with 2nd highest salary:", name_second, top2)