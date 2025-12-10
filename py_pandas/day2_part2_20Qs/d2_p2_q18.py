# From a string containing mixed characters, extract only the digits and return them as an integer. Example: "a1b23c9" 1239

def extract_digits(s):
    digits = "".join(a for a in s if a.isdigit())
    return int(digits)

print(extract_digits("a1b23c9d10e11"))
