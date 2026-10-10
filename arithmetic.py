def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

def modulo(a, b):
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a % b

def power(a, b):
    result = a ** b

    if isinstance(result, complex):
        raise ValueError("Результат не является действительным числом")

    return result