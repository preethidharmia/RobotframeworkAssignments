# Create a decorator that logs the execution time of any function it wraps. Demonstrate with a sample slow function.

import time

def timer(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Execution time:", time.time() - start)
        return result
    return wrap

@timer
def slow_function():
    time.sleep(2)

slow_function()
