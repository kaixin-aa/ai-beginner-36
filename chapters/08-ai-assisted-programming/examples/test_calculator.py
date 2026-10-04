import unittest

from calculator_after import calculate


class CalculatorTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate(8, "+", 2), 10)

    def test_subtraction(self):
        self.assertEqual(calculate(8, "-", 2), 6)

    def test_multiplication(self):
        self.assertEqual(calculate(8, "*", 2), 16)

    def test_division(self):
        self.assertEqual(calculate(8, "/", 2), 4)

    def test_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "除数不能为 0"):
            calculate(8, "/", 0)

    def test_unsupported_operator(self):
        with self.assertRaisesRegex(ValueError, "不支持的运算符"):
            calculate(8, "%", 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
