from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd

CHAPTER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHAPTER / "examples"))
from analysis import load_records, summarize


class ExplorationTests(unittest.TestCase):
    def setUp(self):
        self.frame = load_records(CHAPTER / "data/learning_records.csv")

    def test_histogram_and_missing_policy(self):
        result = summarize(self.frame)
        self.assertEqual((result["input_rows"], result["known_minutes_rows"], result["missing_minutes_rows"]), (5, 3, 2))
        self.assertEqual(result["histogram_counts"], [0, 1, 1, 0, 1])
        self.assertEqual(result["known_total"], 75)
        self.assertEqual((result["known_mean"], result["known_median"]), (25, 20))

    def test_group_denominators(self):
        groups = {row["tag"]: row for row in summarize(self.frame)["groups"]}
        self.assertEqual((groups["python"]["records"], groups["python"]["completed"]), (3, 2))
        self.assertAlmostEqual(groups["python"]["completion_rate"], 2/3)
        self.assertEqual((groups["ai"]["records"], groups["ai"]["completed"]), (2, 1))
        self.assertEqual(groups["ai"]["completion_rate"], 0.5)
        self.assertEqual(groups["python"]["missing_minutes"], 1)

    def test_scatter_pairing_and_correlation(self):
        result = summarize(self.frame)
        self.assertEqual([point["record_id"] for point in result["scatter_points"]], ["L01", "L02", "L05"])
        self.assertAlmostEqual(result["pearson_r"], 0.6546536707079771)

    def test_undefined_correlation(self):
        frame = self.frame.copy()
        frame["done"] = True
        self.assertIsNone(summarize(frame)["pearson_r"])
        frame["minutes"] = pd.NA
        result = summarize(frame)
        self.assertIsNone(result["known_mean"])
        self.assertIsNone(result["pearson_r"])

    def test_empty(self):
        result = summarize(self.frame.iloc[:0])
        self.assertEqual(result["histogram_counts"], [0]*5)
        self.assertEqual(result["groups"], [])

    def test_bins_do_not_silently_drop_long_records(self):
        frame = self.frame.copy()
        frame.loc[0, "minutes"] = 80
        with self.assertRaisesRegex(ValueError, "扩展 BINS"):
            summarize(frame)

    def test_invalid_numeric_input(self):
        for value in (-1, np.inf, 1441):
            with tempfile.TemporaryDirectory() as directory:
                frame = self.frame.copy()
                frame.loc[0, "minutes"] = value
                target = Path(directory) / "bad.csv"
                frame.to_csv(target, index=False)
                with self.subTest(value=value), self.assertRaises(ValueError):
                    load_records(target)


if __name__ == "__main__":
    unittest.main()
