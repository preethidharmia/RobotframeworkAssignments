# Given two lists, write a program to find elements that exist in both lists (intersection) without using set operations.

def intersect(l1, l2):
    result = []
    for x in l1:
        if x in l2 and x not in result:
            result.append(x)
    return result

print(intersect([1,2,3], [2,3,4]))
