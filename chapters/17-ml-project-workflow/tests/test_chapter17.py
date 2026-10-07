import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from project_core import FEATURES, load_dataset, split_dataset, train_project, predict_one, validate_frame
from model_io import save_model, load_model


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = load_dataset()
        cls.model, cls.train, cls.test, cls.summary = train_project(cls.frame)

    def test_public_snapshot_dimensions(self):
        self.assertEqual(self.frame.shape, (150, 6))
        self.assertEqual(self.frame["target"].value_counts().sort_index().tolist(), [50, 50, 50])

    def test_disjoint_complete_stratified_split(self):
        self.assertEqual((len(self.train), len(self.test)), (120, 30))
        self.assertTrue(set(self.train.sample_id).isdisjoint(self.test.sample_id))
        self.assertEqual(set(self.train.sample_id) | set(self.test.sample_id), set(self.frame.sample_id))
        self.assertEqual(self.summary["train_class_counts"], [40, 40, 40])
        self.assertEqual(self.summary["test_class_counts"], [10, 10, 10])

    def test_split_reproducible(self):
        a, b = split_dataset(self.frame)
        self.assertEqual(a.sample_id.tolist(), self.train.sample_id.tolist())
        self.assertEqual(b.sample_id.tolist(), self.test.sample_id.tolist())

    def test_scaler_uses_training_only(self):
        scaler = self.model.named_steps["scale"]
        self.assertEqual(scaler.n_samples_seen_, 120)
        np.testing.assert_allclose(scaler.mean_, self.train[FEATURES].mean().to_numpy())
        self.assertFalse(np.allclose(scaler.mean_, self.frame[FEATURES].mean().to_numpy()))

    def test_features_and_labels_stay_paired(self):
        original = self.frame.set_index("sample_id")
        for subset in [self.train, self.test]:
            paired = original.loc[subset["sample_id"]]
            np.testing.assert_array_equal(paired["target"].to_numpy(), subset["target"].to_numpy())
            np.testing.assert_array_equal(paired[FEATURES].to_numpy(), subset[FEATURES].to_numpy())

    def test_metrics_from_actual_predictions(self):
        correct = int(self.test.correct.sum())
        self.assertEqual(correct, self.summary["test_correct"])
        self.assertEqual(correct / len(self.test), self.summary["test_accuracy"])
        self.assertAlmostEqual(self.summary["baseline_test_accuracy"], 1 / 3)
        self.assertGreater(self.summary["test_accuracy"], self.summary["baseline_test_accuracy"])

    def test_save_reload_and_corruption(self):
        with tempfile.TemporaryDirectory() as folder:
            path = save_model(self.model, folder)
            restored = load_model(folder)
            np.testing.assert_array_equal(restored.predict(self.test[FEATURES]), self.test.prediction.to_numpy())
            path.write_bytes(path.read_bytes() + b"changed")
            with self.assertRaisesRegex(ValueError, "校验"):
                load_model(folder)

    def test_version_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            save_model(self.model, folder)
            path = Path(folder) / "model-metadata.json"
            metadata = json.loads(path.read_text(encoding="utf-8"))
            metadata["versions"]["scikit_learn"] = "0.0.0"
            path.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "版本"):
                load_model(folder)

    def test_named_and_positional_inputs(self):
        values = [5.1, 3.5, 1.4, 0.2]
        self.assertEqual(predict_one(self.model, values), predict_one(self.model, dict(zip(FEATURES, values))))
        for invalid in [[5, 3], [5, 3, 1, float("nan")], [5, 3, 1, -1], [[5, 3, 1, 0.2]]]:
            with self.assertRaises(ValueError):
                predict_one(self.model, invalid)

    def test_invalid_dataset_rejected(self):
        for kind in ["missing", "duplicate", "bad_number", "bad_target", "empty"]:
            frame = self.frame.copy()
            if kind == "missing":
                frame = frame.drop(columns=FEATURES[0])
            elif kind == "duplicate":
                frame.loc[1, "sample_id"] = frame.loc[0, "sample_id"]
            elif kind == "bad_number":
                frame.loc[0, FEATURES[0]] = float("inf")
            elif kind == "bad_target":
                frame.loc[0, "target"] = 3
            else:
                frame = frame.iloc[:0]
            with self.assertRaises(ValueError):
                validate_frame(frame)


if __name__ == "__main__":
    unittest.main()
