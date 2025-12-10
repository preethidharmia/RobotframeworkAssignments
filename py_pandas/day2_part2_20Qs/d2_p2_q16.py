# Create a program that simulates rolling two dice and prints the sum for each roll.
# Allow the user to choose number of rolls.

import random

num_rolls = int(input("How many times should I roll the dice? "))

for i in range(1, num_rolls + 1):
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2  # Sum of dice

    print(f"Roll {i}: {d1} + {d2} = {total}")
