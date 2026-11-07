import math
import unittest

import math_functions


class TestMathFunctions(unittest.TestCase):

    # ---------- синус (угол в радианах) ----------

    def test_sin(self):
        self.assertAlmostEqual(math_functions.sin(0), 0)

    def test_sin_special_angles(self):
        cases = [
            (math.pi / 2, 1),
            (math.pi, 0),
            (-math.pi / 2, -1),
            (math.pi / 6, 0.5),
        ]
        for angle, expected in cases:
            with self.subTest(angle=angle):
                self.assertAlmostEqual(math_functions.sin(angle), expected)

    # ---------- косинус (угол в радианах) ----------

    def test_cos(self):
        self.assertAlmostEqual(math_functions.cos(0), 1)

    def test_cos_special_angles(self):
        cases = [
            (math.pi / 2, 0),
            (math.pi, -1),
            (math.pi / 3, 0.5),
        ]
        for angle, expected in cases:
            with self.subTest(angle=angle):
                self.assertAlmostEqual(math_functions.cos(angle), expected)

    def test_sin_cos_identity(self):
        # sin²x + cos²x = 1 для любого x
        for x in (0, 0.5, 1, 2, -3):
            with self.subTest(x=x):
                s = math_functions.sin(x)
                c = math_functions.cos(x)
                self.assertAlmostEqual(s * s + c * c, 1)

    # ---------- квадратный корень ----------

    def test_square_root(self):
        self.assertEqual(math_functions.square_root(25), 5)

    def test_square_root_zero(self):
        self.assertEqual(math_functions.square_root(0), 0)

    def test_square_root_fraction(self):
        self.assertEqual(math_functions.square_root(0.25), 0.5)

    def test_square_root_irrational(self):
        self.assertAlmostEqual(math_functions.square_root(2), 1.41421356, places=7)

    def test_square_root_negative(self):
        with self.assertRaises(ValueError):
            math_functions.square_root(-1)

    def test_square_root_small_negative(self):
        with self.assertRaises(ValueError):
            math_functions.square_root(-0.0001)

    def test_square_root_negative_message(self):
        with self.assertRaisesRegex(ValueError, "отрицательного"):
            math_functions.square_root(-4)

    # ---------- округление вниз ----------

    def test_floor(self):
        self.assertEqual(math_functions.floor(3.8), 3)

    def test_floor_negative(self):
        self.assertEqual(math_functions.floor(-2.3), -3)
        self.assertEqual(math_functions.floor(-0.5), -1)

    def test_floor_integer(self):
        self.assertEqual(math_functions.floor(5), 5)
        self.assertEqual(math_functions.floor(3.0), 3)

    def test_floor_returns_int(self):
        self.assertIsInstance(math_functions.floor(3.8), int)

    # ---------- округление вверх ----------

    def test_ceil(self):
        self.assertEqual(math_functions.ceil(3.2), 4)

    def test_ceil_negative(self):
        self.assertEqual(math_functions.ceil(-2.3), -2)
        self.assertEqual(math_functions.ceil(-0.5), 0)

    def test_ceil_integer(self):
        self.assertEqual(math_functions.ceil(5), 5)
        self.assertEqual(math_functions.ceil(3.0), 3)

    def test_ceil_small_fraction(self):
        self.assertEqual(math_functions.ceil(0.1), 1)

    def test_ceil_returns_int(self):
        self.assertIsInstance(math_functions.ceil(3.2), int)


if __name__ == "__main__":
    unittest.main()
