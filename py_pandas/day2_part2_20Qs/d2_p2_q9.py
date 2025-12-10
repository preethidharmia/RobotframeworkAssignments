# Write a function that takes a string and returns True if it's a palindrome after removing spaces and punctuation.

import re

def is_palindrome(s):
    cleaned = re.sub(r'[^a-z0-9]', '', s.lower())
    return cleaned == cleaned[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"))

# amanaplanacanalpanama
# amanaplanacanalpanama