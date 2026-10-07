from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from regression_core import prepare_data, run_experiment, metrics, FEATURES, ROOT


class RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean, cls.rejected, cls.cleaning = prepare_data()
        cls.models, cls.train, cls.test, cls.summary = run_experiment(cls.clean)

    def test_cleaning_count_and_reasons(self):
        self.assertEqual(self.cleaning["raw_rows"], 205)
        self.assertEqual(len(self.clean)+len(self.rejected), 205)
        self.assertFalse(self.clean[[*FEATURES, "price"]].isna().any().any())
        self.assertTrue((self.rejected.missing_fields != "").all())
        self.assertTrue(set(self.clean.sample_id).isdisjoint(self.rejected.sample_id))

    def test_split_is_disjoint_complete_and_paired(self):
        self.assertTrue(set(self.train.sample_id).isdisjoint(self.test.sample_id))
        self.assertEqual(set(self.train.sample_id) | set(self.test.sample_id), set(self.clean.sample_id))
        original = self.clean.set_index("sample_id")
        for frame in [self.train, self.test]:
            np.testing.assert_array_equal(original.loc[frame.sample_id, "price"].to_numpy(), frame.price.to_numpy())

    def test_baseline_is_training_mean(self):
        np.testing.assert_allclose(self.test.baseline_prediction, self.train.price.mean())
        self.assertFalse(np.isclose(self.train.price.mean(), self.clean.price.mean()))

    def test_metrics_independent_manual_calculation(self):
        residual = self.test.price.to_numpy()-self.test.multi_prediction.to_numpy()
        expected = [np.abs(residual).mean(), np.sqrt(np.mean(residual**2)), 1-np.sum(residual**2)/np.sum((self.test.price-self.test.price.mean())**2)]
        np.testing.assert_allclose(expected, list(self.summary["scores"]["multi"]["test"].values()))

    def test_parameter_prediction_matches_pipeline(self):
        model = self.models["multi"]
        manual = model.intercept_ + self.test[FEATURES].to_numpy() @ model.coef_
        np.testing.assert_allclose(manual, self.test.multi_prediction.to_numpy())

    def test_residual_direction_and_worst_rows(self):
        np.testing.assert_allclose(self.test.multi_residual, self.test.price-self.test.multi_prediction)
        largest = self.test.sort_values("multi_absolute_error", ascending=False).iloc[0]
        self.assertEqual(largest.sample_id, self.summary["worst_multi_test_rows"][0]["sample_id"])

    def test_known_metric_example_and_invalid_inputs(self):
        result = metrics([10000, 20000], [12000, 17000])
        self.assertEqual(result["MAE"], 2500)
        self.assertAlmostEqual(result["RMSE"], np.sqrt(6500000))
        for a, b in [([1], [1]), ([1, 2], [1]), ([1, 2], [1, np.nan])]:
            with self.assertRaises(ValueError):
                metrics(a, b)

    def test_missing_labels_are_rejected_not_imputed(self):
        price_missing = self.rejected["price"].isna()
        self.assertEqual(int(price_missing.sum()), self.cleaning["missing_counts_in_selected_fields"]["price"])

    def test_malformed_file_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text("1,2,3\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "26"):
                prepare_data(path)


if __name__ == "__main__":
    unittest.main()
