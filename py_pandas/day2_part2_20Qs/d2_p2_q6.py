# Write a function that accepts any number of positional arguments and returns their average.
# Test the function with sample inputs.

def avg(*nums):
    return sum(nums) / len(nums)

print(avg(10, 20, 30))
