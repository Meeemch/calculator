import tkinter as tk
import unittest

from main import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.calculator = Calculator(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_input_digit(self):
        self.calculator.input_digit("5")

        self.assertEqual(self.calculator.display_value.get(), "5")

    def test_input_multiple_digits(self):
        self.calculator.input_digit("1")
        self.calculator.input_digit("2")
        self.calculator.input_digit("3")

        self.assertEqual(self.calculator.display_value.get(), "123")

    def test_input_decimal(self):
        self.calculator.input_decimal()

        self.assertEqual(self.calculator.display_value.get(), "0.")

    def test_clear(self):
        self.calculator.display_value.set("123")
        self.calculator.first_operand = 10
        self.calculator.pending_operator = "+"

        self.calculator.clear()

        self.assertEqual(self.calculator.display_value.get(), "0")
        self.assertIsNone(self.calculator.first_operand)
        self.assertIsNone(self.calculator.pending_operator)
        self.assertIs(self.calculator.new_input, True)

    def test_delete_last(self):
        self.calculator.display_value.set("123")
        self.calculator.new_input = False

        self.calculator.delete_last()

        self.assertEqual(self.calculator.display_value.get(), "12")

    def test_change_sign(self):
        self.calculator.display_value.set("5")

        self.calculator.change_sign()

        self.assertEqual(self.calculator.display_value.get(), "-5")

    def test_addition(self):
        self.calculator.display_value.set("2")
        self.calculator.set_operator("+")

        self.calculator.display_value.set("3")
        self.calculator.new_input = False

        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "5")

    def test_subtraction(self):
        self.calculator.display_value.set("8")
        self.calculator.set_operator("−")

        self.calculator.display_value.set("3")
        self.calculator.new_input = False

        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "5")

    def test_multiplication(self):
        self.calculator.display_value.set("4")
        self.calculator.set_operator("×")

        self.calculator.display_value.set("5")
        self.calculator.new_input = False

        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "20")

    def test_division(self):
        self.calculator.display_value.set("10")
        self.calculator.set_operator("÷")

        self.calculator.display_value.set("2")
        self.calculator.new_input = False

        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "5")

    def test_memory_operations(self):
        self.calculator.display_value.set("10")
        self.calculator.memory_operation("M+")

        self.assertEqual(self.calculator.memory, 10)

        self.calculator.display_value.set("3")
        self.calculator.memory_operation("M-")

        self.assertEqual(self.calculator.memory, 7)

        self.calculator.memory_operation("MC")

        self.assertEqual(self.calculator.memory, 0)

    def test_memory_recall(self):
        self.calculator.memory = 25

        self.calculator.memory_operation("MR")

        self.assertEqual(self.calculator.display_value.get(), "25")
        self.assertIs(self.calculator.new_input, True)

    def test_unary_square_root(self):
        self.calculator.display_value.set("9")

        self.calculator.unary_operation("√")

        self.assertEqual(self.calculator.display_value.get(), "3")

    def test_unary_sin(self):
        self.calculator.display_value.set("0")

        self.calculator.unary_operation("sin")

        self.assertEqual(self.calculator.display_value.get(), "0")

    def test_unary_negative_square_root(self):
        self.calculator.display_value.set("-1")

        with self.assertRaises(ValueError):
            self.calculator.unary_operation("√")

    def test_format_number(self):
        self.assertEqual(self.calculator.format_number(5.0), "5")
        self.assertEqual(self.calculator.format_number(0), "0")
        self.assertEqual(self.calculator.format_number(2.5), "2.5")


if __name__ == "__main__":
    unittest.main()