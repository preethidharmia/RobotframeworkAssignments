# Write a function to find the longest word in a list of strings.

def longest_word(words):
    return max(words, key=len)

print(longest_word(["apple", "watermelon", "kiwi", "Dragon Fruit", "Blackberry"]))
