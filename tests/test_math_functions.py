import math
import unittest

import math_functions


class TestMathFunctions(unittest.TestCase):

    def test_sin(self):
        self.assertAlmostEqual(math_functions.sin(0), 0)

    def test_cos(self):
        self.assertAlmostEqual(math_functions.cos(0), 1)

    def test_square_root(self):
        self.assertEqual(math_functions.square_root(25), 5)

    def test_square_root_negative(self):
        with self.assertRaises(ValueError):
            math_functions.square_root(-1)

    def test_floor(self):
        self.assertEqual(math_functions.floor(3.8), 3)

    def test_ceil(self):
        self.assertEqual(math_functions.ceil(3.2), 4)


if __name__ == "__main__":
    unittest.main()