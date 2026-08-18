"""
    PYTHON STRINGS - "" or ''
"""

print("hello!")
print('hello!')
print('\n---\n')

# Assign String to a Variable
a = "Hello"
print(a)
print('\n---\n')

# Multiline Strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
print('\n---\n')

# Note : 
# - You can assign a multiline string to a variable by using three quotes
# - in the result, the line breaks are inserted at the same position as in the code.

# Strings are Arrays []
a = "Hello, World!"
print(a[1])
print('\n---\n')

# Looping Through a String
for x in a:
    print(x)
print('\n---\n')

# String Length
print(len(a))
print('\n---\n')

# Check String :: keyworld 'in' or IF statement
txt = "The best things in life are free!"
print("free" in txt)

if "free" in txt:
    print