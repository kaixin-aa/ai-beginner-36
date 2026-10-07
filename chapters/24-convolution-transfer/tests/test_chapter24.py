import json
import sys
from pathlib import Path
import unittest
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"examples"))
from conv_core import ROOT, TEACHING_IMAGE, TEACHING_KERNEL, manual_correlation, ParityImages, TinyCNN, load_manifest, configure, freeze_features, fit, target_model, load_target


class Chapter24Tests(unittest.TestCase):
    def test_01_disjoint_roles_and_class_balance(self):
        rows = load_manifest()
        roles = {name:{int(r["source_id"]) for r in rows if r["role"] == name} for name in ["pretrain","target_train","target_test","unused"]}
        self.assertEqual(len(set.union(*roles.values())),1797)
        for left in roles:
            for right in roles:
                if left != right:
                    self.assertFalse(roles[left] & roles[right])
        for role, each in [("target_train",60),("target_test",100)]:
            self.assertEqual([sum(r["role"]==role and int(r["target_label"])==label for r in rows) for label in [0,1]],[each,each])

    def test_02_all_png_values_and_label_provenance(self):
        with np.load(ROOT/"data/original-digits.npz",allow_pickle=False) as original:
            for role in ["target_train","target_test"]:
                dataset = ParityImages(role)
                for i,row in enumerate(dataset.rows):
                    x,label = dataset[i]
                    source_id = int(row["source_id"])
                    np.testing.assert_array_equal(x.numpy()[0],original["images"][source_id]/16)
                    self.assertEqual(label,int(original["labels"][source_id])%2)

    def test_03_manual_convolution_independent_expected(self):
        expected = np.array([[-2,0,1],[0,1,0],[0,0,0]],dtype=np.float32)
        np.testing.assert_array_equal(manual_correlation(TEACHING_IMAGE,TEACHING_KERNEL),expected)
        actual = torch.nn.functional.conv2d(torch.tensor(TEACHING_IMAGE)[None,None],torch.tensor(TEACHING_KERNEL)[None,None])
        np.testing.assert_array_equal(actual[0,0].numpy(),expected)

    def test_04_pooling_and_shapes(self):
        image = torch.tensor(TEACHING_IMAGE)[None,None]
        np.testing.assert_array_equal(torch.nn.MaxPool2d(2)(image)[0,0].numpy(),[[3,2],[1,2]])
        model = TinyCNN(2)
        self.assertEqual(tuple(model(torch.zeros(4,1,8,8)).shape),(4,2))
        self.assertEqual(sum(p.numel() for p in model.parameters()),4274)
        freeze_features(model)
        self.assertEqual(sum(p.numel() for p in model.parameters() if p.requires_grad),66)

    def test_05_frozen_training_really_preserves_features(self):
        configure(42)
        model = TinyCNN(2)
        before = {k:v.clone() for k,v in model.features.state_dict().items()}
        head = model.head.weight.clone()
        x = torch.ones(4,1,8,8)
        history,timing = fit(model,x,torch.tensor([0,0,0,1]),1,42,"frozen",batch_size=2)
        self.assertEqual(timing["updates"],2)
        self.assertTrue(all(torch.equal(v,model.features.state_dict()[k]) for k,v in before.items()))
        self.assertFalse(torch.equal(head,model.head.weight))

    def test_06_target_heads_identical_before_training(self):
        source = TinyCNN(10)
        models = [target_model(mode,source) for mode in ["scratch","frozen","fine_tune"]]
        for model in models[1:]:
            self.assertTrue(torch.equal(model.head.weight,models[0].head.weight))
            self.assertTrue(torch.equal(model.head.bias,models[0].head.bias))

    def test_07_saved_transfer_features_provenance(self):
        source = torch.load(ROOT/"results/pretrained-digits.pt",weights_only=True)
        frozen = load_target(ROOT/"results/frozen-state.pt")
        self.assertTrue(all(torch.equal(v,frozen.features.state_dict()[k]) for k,v in source["features"].items()))
        tuned = load_target(ROOT/"results/fine_tune-state.pt")
        self.assertTrue(any(not torch.equal(v,tuned.features.state_dict()[k]) for k,v in source["features"].items()))

    def test_08_comparison_fixed_budget_and_independent_counts(self):
        summary = json.loads((ROOT/"results/comparison-summary.json").read_text(encoding="utf-8"))
        self.assertTrue(summary["initial_target_heads_identical"])
        self.assertFalse(summary["test_used_for_training_or_selection"])
        import csv
        with (ROOT/"results/test-predictions.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows),200)
        for record in summary["experiments"]:
            mode = record["mode"]
            self.assertEqual(record["epochs"],20)
            self.assertEqual(record["updates"],80)
            self.assertTrue(record["reload_logits_identical"])
            self.assertEqual(sum(row[mode]==row["true_parity"] for row in rows),record["test"]["correct"])
            self.assertGreater(record["test"]["correct"],100)

    def test_09_invalid_settings_and_oversize_kernel(self):
        with self.assertRaises(ValueError):
            manual_correlation(np.zeros((2,2)),np.zeros((3,3)))
        with self.assertRaises(ValueError):
            ParityImages("pretrain")
        with self.assertRaises(ValueError):
            fit(TinyCNN(2),torch.zeros(1,1,8,8),torch.tensor([0]),0,42)


if __name__ == "__main__":
    unittest.main()
