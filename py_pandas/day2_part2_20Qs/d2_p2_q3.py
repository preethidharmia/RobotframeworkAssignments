# Create a generator function that yields even numbers up to a given limit. Show how to iterate over it and print results.

def even_gen(limit):
    for num in range(0, limit + 1, 2):
        yield num

for n in even_gen(10):
    print(n)
