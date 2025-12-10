# Given a list of integers, separate them into two lists: one containing even numbers and the other containing odd numbers.

def split_even_odd(lst):
    evens = []
    odds = []
    for n in lst:
        (evens if n % 2 == 0 else odds).append(n)
    return evens, odds

print(split_even_odd(range(20)))