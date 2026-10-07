from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
import torch
from torch import nn
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"examples"))
from image_core import ROOT, load_snapshot, pixels_to_tensor, load_single_image, make_model, train_model, load_model, save_model, predict_image


class ImageTests(unittest.TestCase):
    def test_snapshot_and_disjoint_split(self):
        images, labels, train, test = load_snapshot()
        self.assertEqual(images.shape, (1797, 8, 8))
        self.assertEqual((len(train), len(test)), (1437, 360))
        self.assertTrue(set(train).isdisjoint(test))
        np.testing.assert_array_equal(np.sort(np.r_[train, test]), np.arange(1797))
        self.assertEqual(set(labels[train]), set(range(10)))
        self.assertEqual(set(labels[test]), set(range(10)))

    def test_png_npy_preprocessing_identical(self):
        a = load_single_image(ROOT/"data/sample-digit.png")
        b = load_single_image(ROOT/"data/sample-digit.npy")
        self.assertTrue(torch.equal(a, b))
        self.assertEqual(tuple(a.shape), (1, 1, 8, 8))
        self.assertEqual(a.dtype, torch.float32)

    def test_normalization_bounds_and_invalid_images(self):
        values = np.full((8, 8), 16)
        self.assertEqual(pixels_to_tensor(values).max().item(), 1)
        for bad in [np.zeros((28, 28)), np.full((8, 8), 255), np.full((8, 8), np.nan), np.zeros((0, 8, 8))]:
            with self.assertRaises(ValueError):
                pixels_to_tensor(bad)

    def test_network_output_and_parameter_count(self):
        model = make_model()
        self.assertEqual(tuple(model(torch.zeros(4, 1, 8, 8)).shape), (4, 10))
        self.assertEqual(sum(p.numel() for p in model.parameters()), 2410)

    def test_cross_entropy_matches_log_softmax(self):
        logits = torch.tensor([[1., 0., -1.]], dtype=torch.float64)
        loss = nn.CrossEntropyLoss()(logits, torch.tensor([0]))
        expected = -torch.log_softmax(logits, dim=1)[0, 0]
        self.assertAlmostEqual(loss.item(), expected.item(), places=12)

    def test_batch_steps_and_seed_reproducibility(self):
        a = train_model(epochs=1)
        b = train_model(epochs=1)
        self.assertEqual(a[-1]["optimizer_updates"], 23)
        self.assertEqual(a[-1]["last_batch_rows"], 29)
        np.testing.assert_array_equal(a[5], b[5])
        for key in a[0].state_dict():
            self.assertTrue(torch.equal(a[0].state_dict()[key], b[0].state_dict()[key]))

    def test_saved_model_and_probabilities(self):
        model = load_model(ROOT/"results/digits-state.pt")
        images, labels, train, test = load_snapshot()
        with torch.no_grad():
            correct = int((model(pixels_to_tensor(images[test])).argmax(1) == torch.tensor(labels[test])).sum())
        self.assertGreater(correct, 300)
        prediction = predict_image(model, load_single_image(ROOT/"data/sample-digit.png"))
        self.assertEqual(len(prediction["probabilities"]), 10)
        self.assertAlmostEqual(sum(prediction["probabilities"]), 1, places=6)
        self.assertEqual(prediction["label"], int(np.argmax(prediction["probabilities"])))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"model.pt"
            save_model(model, path)
            clone = load_model(path)
            self.assertTrue(torch.equal(model(pixels_to_tensor(images[test])), clone(pixels_to_tensor(images[test]))))

    def test_invalid_training_configuration(self):
        for kwargs in [{"epochs": True}, {"batch_size": 0}, {"learning_rate": -0.1}]:
            with self.assertRaises(ValueError):
                train_model(**kwargs)


if __name__ == "__main__":
    unittest.main()
