import math


def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def square_root(x):
    if x < 0:
        raise ValueError(
            "Нельзя извлечь корень из отрицательного числа"
        )
    return math.sqrt(x)