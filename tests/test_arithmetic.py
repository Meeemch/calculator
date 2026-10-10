import unittest

import arithmetic


class TestArithmetic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(arithmetic.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(arithmetic.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(arithmetic.multiply(4, 3), 12)

    def test_divide(self):
        self.assertEqual(arithmetic.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            arithmetic.divide(10, 0)

    def test_modulo(self):
        self.assertEqual(arithmetic.modulo(10, 3), 1)

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            arithmetic.modulo(10, 0)

    def test_power(self):
        self.assertEqual(arithmetic.power(2, 3), 8)


if __name__ == "__main__":
    unittest.main()