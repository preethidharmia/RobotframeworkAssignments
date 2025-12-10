# Write a program that counts how many times each word occurs in a paragraph of text.
# Ignore punctuation and treat words in a case-insensitive way.
import re
from collections import Counter

def word_count(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

para = "Hello world! Hello Python. repeat-ing repeat-ed words are also words."
print(word_count(para))