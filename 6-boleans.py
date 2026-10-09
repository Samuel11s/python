"""
    PYTHON BOLEANS - True or False
"""

# Boolean Values

print(10 > 9) # True
print(10 == 9) # False
print(10 < 9) # False
print("---")

## Print a message based on whether the condition is True or False:
a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")


print("---")

# Evaluate Values and Variables - bool() function returns True or False
## Evaluate a string and a number:
print(bool("Hello"))
print(bool(15))
print("---")

## Evaluate two variables:
x = "Hello"
y = 15
print(bool(x))
print(bool(y))
print("---")

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
print("---")

# Functions can Return a Boolean
def myFunction() :
    return True

print(myFunction()) # True
print("---")

## Code based on the Boolean answer of a function
def myFunction():
    return True

if myFunction():
    print("YES!")
else:
    print("NO!")
    
print("---")

# Python also has many built-in functions that return a boolean value, like the isinstance() function, which can be used to determine if an object is of a certain data type:
## Check if an object is an integer or not:
x = 200
print(isinstance(x, int))