import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from math_core import loss, gradient, finite_difference, descent


class MathTests(unittest.TestCase):
    def test_same_mean_different_variance(self):
        a, b = np.array([18, 20, 22]), np.array([10, 20, 30])
        self.assertEqual(a.mean(), b.mean())
        self.assertAlmostEqual(a.var(), 8 / 3)
        self.assertAlmostEqual(b.var(), 200 / 3)
        self.assertEqual(a.var(ddof=1), 4)

    def test_fair_die_probability(self):
        p = np.full(6, 1/6)
        self.assertAlmostEqual(p.sum(), 1)
        self.assertAlmostEqual(p[[1, 3, 5]].sum(), 0.5)

    def test_derivative_matches_central_difference(self):
        for w in [-2, 1, 3, 5, 9]:
            self.assertAlmostEqual(finite_difference(w), gradient(w), places=8)

    def test_first_updates(self):
        rows = descent(9, 0.2, 3)
        np.testing.assert_allclose([r["w"] for r in rows], [9, 6.6, 5.16, 4.296])
        np.testing.assert_allclose([r["loss"] for r in rows], [37, 13.96, 5.6656, 2.679616])

    def test_descent_and_optimum(self):
        rows = descent()
        self.assertTrue(all(b["loss"] < a["loss"] for a, b in zip(rows, rows[1:])))
        self.assertLess(rows[-1]["loss"], 1.001)
        self.assertEqual(descent(3, 0.2, 3)[-1]["w"], 3)
        self.assertEqual(loss(3), 1)

    def test_overshoot_and_oscillation(self):
        rows = descent(9, 1.1, 2)
        self.assertGreater(rows[1]["loss"], rows[0]["loss"])
        self.assertGreater(rows[2]["loss"], rows[1]["loss"])
        self.assertEqual([r["w"] for r in descent(9, 1.0, 2)], [9, -3, 9])
        self.assertEqual(descent(9, 0.5, 1)[-1]["w"], 3)

    def test_zero_steps_and_left_side(self):
        self.assertEqual(len(descent(9, 0.2, 0)), 1)
        self.assertEqual([r["w"] for r in descent(1, 0.25, 2)], [1, 2, 2.5])

    def test_invalid_inputs(self):
        for value in [True, "9", float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                loss(value)
        for rate in [0, -1, float("inf")]:
            with self.assertRaises(ValueError):
                descent(9, rate)
        for steps in [True, -1, 1.5]:
            with self.assertRaises(ValueError):
                descent(steps=steps)
        with self.assertRaises(ValueError):
            finite_difference(5, 0)


if __name__ == "__main__":
    unittest.main()
