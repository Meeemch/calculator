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


    # ---------- дополнительные случаи: ввод ----------

    def test_initial_state(self):
        self.assertEqual(self.calculator.display_value.get(), "0")
        self.assertIsNone(self.calculator.first_operand)
        self.assertIsNone(self.calculator.pending_operator)
        self.assertEqual(self.calculator.memory, 0)

    def test_leading_zero_replaced(self):
        self.calculator.input_digit("0")
        self.calculator.input_digit("0")
        self.calculator.input_digit("7")

        self.assertEqual(self.calculator.display_value.get(), "7")

    def test_decimal_number(self):
        self.calculator.input_digit("3")
        self.calculator.input_decimal()
        self.calculator.input_digit("1")
        self.calculator.input_digit("4")

        self.assertEqual(self.calculator.display_value.get(), "3.14")

    def test_second_decimal_point_ignored(self):
        self.calculator.input_digit("1")
        self.calculator.input_decimal()
        self.calculator.input_digit("5")
        self.calculator.input_decimal()

        self.assertEqual(self.calculator.display_value.get(), "1.5")

    def test_input_after_result_starts_new_number(self):
        self.calculator.display_value.set("2")
        self.calculator.set_operator("+")
        self.calculator.display_value.set("3")
        self.calculator.new_input = False
        self.calculator.equals()

        self.calculator.input_digit("7")

        self.assertEqual(self.calculator.display_value.get(), "7")

    # ---------- дополнительные случаи: удаление и знак ----------

    def test_delete_last_single_digit(self):
        self.calculator.display_value.set("7")
        self.calculator.new_input = False

        self.calculator.delete_last()

        self.assertEqual(self.calculator.display_value.get(), "0")

    def test_delete_last_negative_single_digit(self):
        self.calculator.display_value.set("-5")
        self.calculator.new_input = False

        self.calculator.delete_last()

        self.assertEqual(self.calculator.display_value.get(), "0")

    def test_delete_last_ignored_after_result(self):
        self.calculator.display_value.set("123")
        self.calculator.new_input = True

        self.calculator.delete_last()

        self.assertEqual(self.calculator.display_value.get(), "123")

    def test_change_sign_twice(self):
        self.calculator.display_value.set("5")

        self.calculator.change_sign()
        self.calculator.change_sign()

        self.assertEqual(self.calculator.display_value.get(), "5")

    def test_change_sign_float(self):
        self.calculator.display_value.set("2.5")

        self.calculator.change_sign()

        self.assertEqual(self.calculator.display_value.get(), "-2.5")

    def test_clear_keeps_memory(self):
        self.calculator.memory = 42
        self.calculator.display_value.set("10")

        self.calculator.clear()

        self.assertEqual(self.calculator.memory, 42)

    # ---------- дополнительные случаи: вычисления ----------

    def _calculate(self, a, operator, b):
        """Набирает a, операцию, b и нажимает «=». Возвращает текст на экране."""
        self.calculator.display_value.set(a)
        self.calculator.set_operator(operator)
        self.calculator.display_value.set(b)
        self.calculator.new_input = False
        self.calculator.equals()
        return self.calculator.display_value.get()

    def test_all_operators(self):
        cases = [
            ("7", "+", "8", "15"),
            ("3", "−", "10", "-7"),
            ("-4", "×", "2.5", "-10"),
            ("1", "÷", "4", "0.25"),
            ("10", "%", "3", "1"),
            ("2", "^", "10", "1024"),
        ]
        for a, operator, b, expected in cases:
            with self.subTest(expression=f"{a} {operator} {b}"):
                self.calculator.clear()
                self.assertEqual(self._calculate(a, operator, b), expected)

    def test_float_result_rounded_for_display(self):
        self.assertEqual(self._calculate("0.1", "+", "0.2"), "0.3")

    def test_division_periodic_fraction(self):
        self.assertEqual(self._calculate("1", "÷", "3"), "0.3333333333")

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            self._calculate("5", "÷", "0")

    def test_modulo_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            self._calculate("5", "%", "0")

    def test_chained_operations(self):
        # 2 + 3 × 4 = считается по порядку: (2 + 3) × 4 = 20
        self.calculator.display_value.set("2")
        self.calculator.set_operator("+")
        self.calculator.display_value.set("3")
        self.calculator.new_input = False
        self.calculator.set_operator("×")

        self.assertEqual(self.calculator.display_value.get(), "5")

        self.calculator.display_value.set("4")
        self.calculator.new_input = False
        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "20")

    def test_change_operator_before_second_number(self):
        # нажали «+», передумали и нажали «×» — должна сработать последняя операция
        self.calculator.display_value.set("6")
        self.calculator.set_operator("+")
        self.calculator.set_operator("×")
        self.calculator.display_value.set("2")
        self.calculator.new_input = False
        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "12")

    def test_equals_without_operator(self):
        self.calculator.display_value.set("42")

        self.calculator.equals()

        self.assertEqual(self.calculator.display_value.get(), "42")

    def test_equals_resets_state(self):
        self._calculate("2", "+", "2")

        self.assertIsNone(self.calculator.first_operand)
        self.assertIsNone(self.calculator.pending_operator)
        self.assertIs(self.calculator.new_input, True)

    # ---------- дополнительные случаи: функции одного числа ----------

    def test_unary_operations(self):
        cases = [
            ("cos", "0", "1"),
            ("√", "2", "1.414213562"),
            ("√", "0", "0"),
            ("floor", "3.7", "3"),
            ("floor", "-3.2", "-4"),
            ("ceil", "3.2", "4"),
            ("ceil", "-3.7", "-3"),
        ]
        for operation, value, expected in cases:
            with self.subTest(operation=operation, value=value):
                self.calculator.display_value.set(value)
                self.calculator.unary_operation(operation)
                self.assertEqual(self.calculator.display_value.get(), expected)

    def test_unary_sets_new_input(self):
        self.calculator.display_value.set("9")
        self.calculator.unary_operation("√")

        self.calculator.input_digit("1")

        self.assertEqual(self.calculator.display_value.get(), "1")

    # ---------- дополнительные случаи: память ----------

    def test_memory_add_twice(self):
        self.calculator.display_value.set("10")
        self.calculator.memory_operation("M+")
        self.calculator.display_value.set("5")
        self.calculator.memory_operation("M+")

        self.assertEqual(self.calculator.memory, 15)

    def test_memory_can_be_negative(self):
        self.calculator.display_value.set("3")
        self.calculator.memory_operation("M-")

        self.assertEqual(self.calculator.memory, -3)

    def test_memory_recall_float(self):
        self.calculator.memory = 2.5

        self.calculator.memory_operation("MR")

        self.assertEqual(self.calculator.display_value.get(), "2.5")

    def test_memory_does_not_change_display(self):
        self.calculator.display_value.set("8")

        self.calculator.memory_operation("M+")

        self.assertEqual(self.calculator.display_value.get(), "8")

    # ---------- дополнительные случаи: формат числа ----------

    def test_format_number_more(self):
        cases = [
            (7, "7"),
            (-3.0, "-3"),
            (0.1 + 0.2, "0.3"),
            (1 / 3, "0.3333333333"),
            (1e20, "1e+20"),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(self.calculator.format_number(number), expected)

    # ---------- дополнительные случаи: нажатие кнопок ----------

    def test_button_click_sequence(self):
        for button in ["1", "2", "+", "3", "="]:
            self.calculator.on_button_click(button)

        self.assertEqual(self.calculator.display_value.get(), "15")

    def test_button_click_full_scenario(self):
        # 9 √ → 3, M+ (память 3), C, MR → 3, × 4 = → 12
        for button in ["9", "√", "M+", "C", "MR", "×", "4", "="]:
            self.calculator.on_button_click(button)

        self.assertEqual(self.calculator.display_value.get(), "12")
        self.assertEqual(self.calculator.memory, 3)

    def test_button_click_backspace_and_sign(self):
        for button in ["1", "2", "3", "⌫", "±"]:
            self.calculator.on_button_click(button)

        self.assertEqual(self.calculator.display_value.get(), "-12")


if __name__ == "__main__":
    unittest.main()