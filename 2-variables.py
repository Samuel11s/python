"""
    x = str(5)
    y = int(5)
    z = float(5)
    print(x)
    print(y)
    print(z)
"""
# x, y, z = 5, 'sam', 5.0
# # print(type(x),type(y), type(z))
# print(x, y, z)

# x, y, z = 'Python', 'is', 'awesome !'

"""
    packed_words = [ 'Python', 'is', 'awesome !']
    x, y, z = packed_words
    # print(type(packed_words))
    print(x, y, z)
"""

#  GLOBAL VARIABLES

x = 'awesome'
print('Python is ' + x + ' !') # x before the GLOBAL keyword
def myfunc():
    global x
    x = 'fatastic'
    print('Python is ' + x + ' !') # x after the GLOBAL keyword and into the def

myfunc()
print('Python is ' + x + ' !') # x outside the def and after the GLOBAL keyword