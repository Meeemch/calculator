import pytest

import arithmetic


def test_add():
    assert arithmetic.add(2, 3) == 5
    assert arithmetic.add(-2, 3) == 1
    assert arithmetic.add(2.5, 1.5) == 4.0


def test_subtract():
    assert arithmetic.subtract(5, 3) == 2
    assert arithmetic.subtract(3, 5) == -2
    assert arithmetic.subtract(-2, -3) == 1


def test_multiply():
    assert arithmetic.multiply(3, 4) == 12
    assert arithmetic.multiply(-3, 4) == -12
    assert arithmetic.multiply(0, 5) == 0


def test_divide():
    assert arithmetic.divide(10, 2) == 5
    assert arithmetic.divide(-10, 2) == -5
    assert arithmetic.divide(5, 2) == 2.5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        arithmetic.divide(10, 0)


def test_modulo():
    assert arithmetic.modulo(10, 3) == 1
    assert arithmetic.modulo(8, 4) == 0
    assert arithmetic.modulo(-10, 3) == 2


def test_modulo_by_zero():
    with pytest.raises(ZeroDivisionError):
        arithmetic.modulo(10, 0)


def test_power():
    assert arithmetic.power(2, 3) == 8
    assert arithmetic.power(5, 0) == 1
    assert arithmetic.power(2, -1) == 0.5
    assert arithmetic.power(-2, 2) == 4