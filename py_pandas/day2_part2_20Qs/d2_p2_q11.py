# Write a program to flat_10 a nested list (eg. [1, [2, [3, 4]], 5] - [1, 2, 3, 4, 5]). Use recursion.

def flat_10(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flat_10(item))
        else:
            result.append(item)
    return result

print(flat_10([1, [2, [3, 4]], 5]))
