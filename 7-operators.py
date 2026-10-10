"""
    PYTHON OPERATORS
"""

# Operators are used to perform operations on variables and values.
print(10 + 5)
print("---")

sum1 = 100 + 50     # 150 (100 + 50)
sum2 = sum1 + 250   # 400 (150 + 250)
sum3 = sum2 + sum2  # 800 (400 + 400)
print(sum1)
print(sum2)
print(sum3)
print("---")

"""
Python divides the operators in the following groups:

- Arithmetic operators
- Assignment operators
- Comparison operators
- Logical operators
- Identity operators
- Membership operators
- Bitwise operators

"""

# Arthmetic Operators - "+ - * / % ** //"
x = 15
y = 4

print(x + y)   # Addition
print(x - y)   # Substraction
print(x * y)   # Multiplication
print(x / y)   # Division   -- return a float
print(x % y)   # Modulus 
print(x ** y)  # Exponentiation
print(x // y)  # Floor division  -- returns an intenger
print("---")

# Assigment Operators - "= += -= *= /= %= //= **= &= |= ^= >>= <<= :="
# Assigment Operators are used to assign values to variables

# &=	x &= 3	x = x & 3
x = 5
x &= 3
print(x)

# The Walrus Operator - ":="
# Python 3.8 introduced the := operator, known as the "walrus operator". 
# It assigns values to variables as part of a larger expression
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3: # same as count = len(numbers) then if count > 3
    print(f"List has {count} elements")