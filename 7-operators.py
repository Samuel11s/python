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

print("---")

# Ternary Operator
# The  Tenary Operator allows you to assign one value if a condition is true, and another if it is false
num = 6

x = "WEEKEND!" if num > 5 else "Workday" # can be used instead of elif in longer if statements
print(x)
print("---")

# Comparaison operators - "== != > < >= <="
#    ==	  Equal	                      x == y	
#.   !=	  Not equal	                  x != y	
#    >	  Greater than	              x > y	
#    <	  Less than	                  x < y	
#    >=	  Greater than or equal to	  x >= y	
#    <=	  Less than or equal to	      x <= y

# Logical operators - "and", "or", "not"
# Operator	Description                                                     Example	Try it
# and 	    Returns True if both statements are true	                    x < 5 and  x < 10	
# or	    Returns True if one of the statements is true	                x < 5 or x < 4	
# not	    Reverse the result, returns False if the result is true	        not(x < 5 and x < 10)

# Identity operators - "is" and "is not"
# Operator	Description	                                                    Example
# is 	    Returns True if both variables are the same object	            x is y	
# is not	Returns True if both variables are not the same object	        x is not y
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is y)       # False
print(x is z)       # True
print(x is not y)   # True
# Difference between "is" and "=="
print(x == y)       # True (they have the same content)
print(x is y)       # False (they are not the same object)
print(z is x)       # True (z is the same object as x)
print("---")

# Membership operators - "in" and "not in"
# Operator	Description	                                                                        Example
# in 	    Returns True if a sequence with the specified value is present in the object	    x in y
# not in	Returns True if a sequence with the specified value is not present in the object	x not in y
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)      # True
# Can also be used with strings !
print("---")

# Bitwise operators - "& | ^ ~ << >>"
# Bitwise operators are used to compare (binary) numbers
# The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0:
print(6 & 3)
# The binary representation of 6 is 0110
# The binary representation of 3 is 0011
# Then the & operator compares the bits and returns 0010, which is 2 in decimal.

# Operator Precedence - "() ** +x -x ~x * / % // + - << >> & ^ | == != < > <= >= is is not in not and or"
# Operator precedence determines the order in which operations are performed in an expression.
print("---")
print(100 + 5 * 3) # 115 (5*3 is evaluated first)
# Addition + and subtraction - has the same precedence, and therefore we evaluate the expression from left to right:
print(5 + 4 - 7 + 3)