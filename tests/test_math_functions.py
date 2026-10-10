import math

import pytest

import math_functions


def test_sin():
    assert math.isclose(math_functions.sin(0), 0)
    assert math.isclose(math_functions.sin(math.pi / 2), 1)
    assert math.isclose(math_functions.sin(-math.pi / 2), -1)


def test_cos():
    assert math.isclose(math_functions.cos(0), 1)
    assert math.isclose(math_functions.cos(math.pi / 2), 0, abs_tol=1e-9)
    assert math.isclose(math_functions.cos(math.pi), -1)


def test_square_root():
    assert math_functions.square_root(0) == 0
    assert math_functions.square_root(9) == 3
    assert math_functions.square_root(2) == pytest.approx(math.sqrt(2))


def test_square_root_negative():
    with pytest.raises(
        ValueError,
        match="Нельзя извлечь корень из отрицательного числа"
    ):
        math_functions.square_root(-1)


def test_floor():
    assert math_functions.floor(3.8) == 3
    assert math_functions.floor(3.0) == 3
    assert math_functions.floor(-2.3) == -3


def test_ceil():
    assert math_functions.ceil(3.2) == 4
    assert math_functions.ceil(3.0) == 3
    assert math_functions.ceil(-2.3) == -2