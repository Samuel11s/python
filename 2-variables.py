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
print('Python is ' + x + ' !') # before the GLOBAL keyword
def myfunc():
    global x
    x = 'fatastic'
    print('Python is ' + x + ' !')

myfunc()
print('Python is ' + x + ' !')