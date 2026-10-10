import math

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def square_root(x):
    if x < 0:
        raise ValueError("Корень из отрицательного числа")
    return math.sqrt(x)

def floor(x):
    return math.floor(x)

def ceil(x):
    return math.ceil(x)
