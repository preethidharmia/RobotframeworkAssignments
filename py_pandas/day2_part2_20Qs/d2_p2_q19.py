# Implement a small module with two functions: one for calculating factorial (using loops), and one using recursion.
# Compare results for a sample number.

def fact_loop(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def fact_rec(n):
    if n == 0:
        return 1
    return n * fact_rec(n-1)

print(fact_loop(5), fact_rec(5))
