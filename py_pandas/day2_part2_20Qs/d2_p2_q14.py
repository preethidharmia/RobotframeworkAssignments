# Given a list of tuples representing student names and scores, sort them by score in descending order.

students = [("Arjun", 70), ("Balaji", 90), ("Chaitra", 80)]
students.sort(key=lambda x: x[1], reverse=True)
print(students)
