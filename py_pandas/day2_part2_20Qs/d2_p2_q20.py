# Write a Python script to check if two given strings are anagrams of each other.
# Ignore spaces and letter case.

import re

def is_anagram(a, b):
    clean = lambda s: sorted(re.sub(r'[^a-z]', '', s.lower()))
    return clean(a) == clean(b)

print(is_anagram("listen", "silent"))
