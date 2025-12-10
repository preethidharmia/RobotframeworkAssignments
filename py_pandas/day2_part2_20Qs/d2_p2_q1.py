# Write a Python function that removes duplicate elements from a list while preserving
# the original order. (Example: [4, 1, 4, 2, 1] - [4, 1, 2])


def remove_dup(lst):
    result = []
    seen = set()
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

print(remove_dup([4, 1, 4, 2, 1]))
