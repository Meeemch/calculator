import pytest
import tkinter as tk

from main import Calculator


@pytest.fixture
def calculator():
    root = tk.Tk()
    root.withdraw()

    calc = Calculator(root)

    yield calc

    root.destroy()


def test_input_digit(calculator):
    calculator.input_digit("5")

    assert calculator.display_value.get() == "5"


def test_input_multiple_digits(calculator):
    calculator.input_digit("1")
    calculator.input_digit("2")
    calculator.input_digit("3")

    assert calculator.display_value.get() == "123"


def test_input_decimal(calculator):
    calculator.input_decimal()

    assert calculator.display_value.get() == "0."


def test_clear(calculator):
    calculator.display_value.set("123")
    calculator.first_operand = 10
    calculator.pending_operator = "+"

    calculator.clear()

    assert calculator.display_value.get() == "0"
    assert calculator.first_operand is None
    assert calculator.pending_operator is None
    assert calculator.new_input is True


def test_delete_last(calculator):
    calculator.display_value.set("123")
    calculator.new_input = False

    calculator.delete_last()

    assert calculator.display_value.get() == "12"


def test_change_sign(calculator):
    calculator.display_value.set("5")

    calculator.change_sign()

    assert calculator.display_value.get() == "-5"


def test_addition(calculator):
    calculator.display_value.set("2")
    calculator.set_operator("+")

    calculator.display_value.set("3")
    calculator.new_input = False

    calculator.equals()

    assert calculator.display_value.get() == "5"


def test_subtraction(calculator):
    calculator.display_value.set("8")
    calculator.set_operator("−")

    calculator.display_value.set("3")
    calculator.new_input = False

    calculator.equals()

    assert calculator.display_value.get() == "5"


def test_multiplication(calculator):
    calculator.display_value.set("4")
    calculator.set_operator("×")

    calculator.display_value.set("5")
    calculator.new_input = False

    calculator.equals()

    assert calculator.display_value.get() == "20"


def test_division(calculator):
    calculator.display_value.set("10")
    calculator.set_operator("÷")

    calculator.display_value.set("2")
    calculator.new_input = False

    calculator.equals()

    assert calculator.display_value.get() == "5"


def test_memory_operations(calculator):
    calculator.display_value.set("10")
    calculator.memory_operation("M+")

    assert calculator.memory == 10

    calculator.display_value.set("3")
    calculator.memory_operation("M-")

    assert calculator.memory == 7

    calculator.memory_operation("MC")

    assert calculator.memory == 0


def test_memory_recall(calculator):
    calculator.memory = 25

    calculator.memory_operation("MR")

    assert calculator.display_value.get() == "25"
    assert calculator.new_input is True


def test_unary_square_root(calculator):
    calculator.display_value.set("9")

    calculator.unary_operation("√")

    assert calculator.display_value.get() == "3"


def test_unary_sin(calculator):
    calculator.display_value.set("0")

    calculator.unary_operation("sin")

    assert calculator.display_value.get() == "0"


def test_unary_negative_square_root(calculator):
    calculator.display_value.set("-1")

    with pytest.raises(ValueError):
        calculator.unary_operation("√")


def test_format_number(calculator):
    assert calculator.format_number(5.0) == "5"
    assert calculator.format_number(0) == "0"
    assert calculator.format_number(2.5) == "2.5"
