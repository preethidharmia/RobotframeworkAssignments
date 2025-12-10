# Write a program to merge two dictionaries. If the same key exists, sum the values.
# Example: ('a': 10) + ('a': 20) ('a': 30)

def merge_dicts(d1, d2):
    result = d1.copy()
    for k, v in d2.items():
        result[k] = result.get(k, 0) + v
    return result

print(merge_dicts({'a':10}, {'a':20, 'b':30}))
