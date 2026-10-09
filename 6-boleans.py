"""
    PYTHON BOLEANS - True or False
"""

# Boolean Values

print(10 > 9) # True
print(10 == 9) # False
print(10 < 9) # False

## Print a message based on whether the condition is True or False:
a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Evaluate Values and Variables - bool() function returns True or False
## Evaluate a string and a number:
print(bool("Hello"))
print(bool(15))

## Evaluate two variables:
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

"""
Most Values are True
Almost any value is evaluated to True if it has some sort of content.
Any string is True, except empty strings.
Any number is True, except 0.
Any list, tuple, set, and dictionary are True, except empty ones.

Some Values are False
In fact, there are not many values that evaluate to False, except empty values, such as (), [], {}, "", the number 0, and the value None. And of course the value False evaluates to False.
"""

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))