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

# Comparaison operators
#    ==	  Equal	                      x == y	
#.   !=	  Not equal	                  x != y	
#    >	  Greater than	              x > y	
#    <	  Less than	                  x < y	
#    >=	  Greater than or equal to	  x >= y	
#    <=	  Less than or equal to	      x <= y

# Logical operators
# Operator	Description                                                     Example	Try it
# and 	    Returns True if both statements are true	                    x < 5 and  x < 10	
# or	    Returns True if one of the statements is true	                x < 5 or x < 4	
# not	    Reverse the result, returns False if the result is true	        not(x < 5 and x < 10)

# Identity operators