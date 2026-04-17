import numpy as np

a = np.array([10, 20, 30, 40, 50])
b = np.array([ 2,  4,  5,  8, 10])

add    = np.add(a, b)         # or a + b
sub    = np.subtract(a, b)    # or a - b
mul    = np.multiply(a, b)    # or a * b
div    = np.divide(a, b)      # or a / b
mod    = np.mod(a, b)         # or a % b
power  = np.power(a, 2)       # square each element

print("a       :", a)
print("b       :", b)
print("add     :", add)
print("subtract:", sub)
print("multiply:", mul)
print("divide  :", div)
print("modulo  :", mod)
print("power^2 :", power)
