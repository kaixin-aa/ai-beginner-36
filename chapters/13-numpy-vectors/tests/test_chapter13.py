from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from score_stats import SCORES, summarize


class ScoreTests(unittest.TestCase):
    def test_means_and_axes(self):
        result = summarize(SCORES)
        np.testing.assert_allclose(result["student_means"], [80, 220/3, 90, 60])
        np.testing.assert_allclose(result["subject_means"], [71.25, 76.25, 80])
        self.assertAlmostEqual(result["overall_mean"], 910/12)
        self.assertEqual(result["shape"], [4, 3])

    def test_broadcast_and_threshold(self):
        result = summarize(SCORES)
        self.assertEqual(result["passed_all"], [True, True, True, False])
        self.assertEqual(result["adjusted_scores"][0], [85, 70, 92])
        self.assertEqual(result["adjusted_scores"][2][0], 100)

    def test_empty_and_bad_shapes(self):
        for array in (np.empty((0, 3)), np.array([80, 90]), np.ones((2, 2))):
            with self.subTest(shape=array.shape), self.assertRaises(ValueError):
                summarize(array)

    def test_invalid_scores(self):
        for value in (-1, 101, np.nan, np.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                summarize([[value, 70, 80]])

    def test_non_numeric(self):
        with self.assertRaises(ValueError):
            summarize([["缺考", 70, 80]])

    def test_view_and_copy(self):
        scores = SCORES.copy()
        view = scores[:, 0]
        view[0] = 1
        self.assertEqual(scores[0, 0], 1)
        copied = scores[:, 1].copy()
        copied[0] = 2
        self.assertEqual(scores[0, 1], 70)


if __name__ == "__main__":
    unittest.main()
