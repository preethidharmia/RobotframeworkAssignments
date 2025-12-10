# Write a Python program to read a CSV file and display only the rows where a specific column meets a given condition.

import csv

def filter_csv(path, column, value):
    with open(path, newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            if row[column] == value:
                print(row)

filter_csv("data.csv", "City", "Chennai")
