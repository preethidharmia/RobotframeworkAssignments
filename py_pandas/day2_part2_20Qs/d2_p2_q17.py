# Write code to remove all occurrences of a specific value from a list without using list comprehensions.

def remove_value(lst, value):
    result = []
    for item in lst:
        if item != value:
            result.append(item)
    return result

print(remove_value([1,2,3,2,4], 2))
