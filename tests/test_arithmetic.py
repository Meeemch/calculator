import unittest

import arithmetic


class TestArithmetic(unittest.TestCase):

    # ---------- сложение ----------

    def test_add(self):
        self.assertEqual(arithmetic.add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(arithmetic.add(-2, 3), 1)
        self.assertEqual(arithmetic.add(-2, -3), -5)

    def test_add_float(self):
        self.assertEqual(arithmetic.add(2.5, 1.5), 4.0)
        self.assertAlmostEqual(arithmetic.add(0.1, 0.2), 0.3)

    def test_add_zero(self):
        self.assertEqual(arithmetic.add(7, 0), 7)

    # ---------- вычитание ----------

    def test_subtract(self):
        self.assertEqual(arithmetic.subtract(5, 3), 2)

    def test_subtract_negative_result(self):
        self.assertEqual(arithmetic.subtract(3, 5), -2)

    def test_subtract_negative_numbers(self):
        self.assertEqual(arithmetic.subtract(-2, -3), 1)

    # ---------- умножение ----------

    def test_multiply(self):
        self.assertEqual(arithmetic.multiply(4, 3), 12)

    def test_multiply_signs(self):
        cases = [
            (-3, 4, -12),
            (3, -4, -12),
            (-3, -4, 12),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(arithmetic.multiply(a, b), expected)

    def test_multiply_by_zero(self):
        self.assertEqual(arithmetic.multiply(0, 5), 0)
        self.assertEqual(arithmetic.multiply(5, 0), 0)

    def test_multiply_float(self):
        self.assertAlmostEqual(arithmetic.multiply(0.5, 0.2), 0.1)

    # ---------- деление ----------

    def test_divide(self):
        self.assertEqual(arithmetic.divide(10, 2), 5)

    def test_divide_float_result(self):
        self.assertEqual(arithmetic.divide(5, 2), 2.5)
        self.assertAlmostEqual(arithmetic.divide(1, 3), 0.3333333333)

    def test_divide_negative(self):
        self.assertEqual(arithmetic.divide(-10, 2), -5)
        self.assertEqual(arithmetic.divide(-10, -2), 5)

    def test_divide_zero_by_number(self):
        self.assertEqual(arithmetic.divide(0, 5), 0)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            arithmetic.divide(10, 0)

    def test_divide_by_float_zero(self):
        with self.assertRaises(ZeroDivisionError):
            arithmetic.divide(10, 0.0)

    def test_divide_by_zero_message(self):
        with self.assertRaisesRegex(ZeroDivisionError, "Деление на ноль"):
            arithmetic.divide(1, 0)

    # ---------- остаток от деления ----------

    def test_modulo(self):
        self.assertEqual(arithmetic.modulo(10, 3), 1)

    def test_modulo_no_remainder(self):
        self.assertEqual(arithmetic.modulo(8, 4), 0)

    def test_modulo_negative(self):
        # в Python остаток имеет знак делителя
        self.assertEqual(arithmetic.modulo(-10, 3), 2)
        self.assertEqual(arithmetic.modulo(10, -3), -2)

    def test_modulo_float(self):
        self.assertEqual(arithmetic.modulo(5.5, 2), 1.5)

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            arithmetic.modulo(10, 0)

    # ---------- степень ----------

    def test_power(self):
        self.assertEqual(arithmetic.power(2, 3), 8)

    def test_power_zero_exponent(self):
        self.assertEqual(arithmetic.power(5, 0), 1)
        self.assertEqual(arithmetic.power(0, 0), 1)

    def test_power_negative_exponent(self):
        self.assertEqual(arithmetic.power(2, -1), 0.5)

    def test_power_negative_base(self):
        self.assertEqual(arithmetic.power(-2, 2), 4)
        self.assertEqual(arithmetic.power(-2, 3), -8)

    def test_power_fractional_exponent(self):
        self.assertEqual(arithmetic.power(9, 0.5), 3.0)


if __name__ == "__main__":
    unittest.main()
