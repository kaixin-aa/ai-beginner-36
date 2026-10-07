import sys
from pathlib import Path
import unittest
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"examples"))
from training_core import *


class Chapter28Tests(unittest.TestCase):
    def test_01_temperature_independent_ratio(self):
        import math
        p = probabilities_at_temperature([2,1,0],.5)
        values = torch.tensor([math.exp(4),math.exp(2),1],dtype=torch.float64)
        torch.testing.assert_close(p,values/values.sum())

    def test_02_entropy_and_argmax(self):
        distributions = [probabilities_at_temperature([2,1,0],temp) for temp in [.5,1,2]]
        self.assertEqual([int(p.argmax()) for p in distributions],[0,0,0])
        self.assertLess(entropy(distributions[0]),entropy(distributions[1]))
        self.assertLess(entropy(distributions[1]),entropy(distributions[2]))

    def test_03_sampling_seed_and_topk(self):
        torch.set_num_threads(1)
        model,tokenizer = load_baseline()
        a = generate(model,tokenizer,"小猫",temperature=2,greedy=False,seed=7,top_k=2)
        b = generate(model,tokenizer,"小猫",temperature=2,greedy=False,seed=7,top_k=2)
        self.assertEqual(a,b)
        for row in a["trace"]:
            self.assertLessEqual(sum(p["probability"]>0 for p in row["top3"]),2)

    def test_04_prompt_targets_excluded(self):
        _,tokenizer = load_baseline()
        x,y = response_only_mask(tokenizer,"我学","编程。")
        self.assertEqual(y[0,:2].tolist(),[-100,-100])
        self.assertEqual(int(y[0,2]),tokenizer.ids["编"])
        self.assertEqual(int(y[0,-1]),tokenizer.eos)
        self.assertEqual(int((y!=-100).sum()),4)

    def test_05_preference_rubric(self):
        pair = load_teaching()["preference_pair"]
        self.assertEqual(sum(row["minutes"] for row in pair["chosen"]),20)
        self.assertEqual(sum(row["minutes"] for row in pair["rejected"]),90)

    def test_06_summary_weights_and_runs(self):
        result = json.loads((ROOT/"results/parameter-summary.json").read_text(encoding="utf-8"))
        self.assertTrue(result["parameters_unchanged"])
        self.assertTrue(result["baseline_file_unchanged"])
        self.assertFalse(result["instruction_training_done"])
        self.assertFalse(result["preference_training_done"])
        self.assertEqual(result["total_generated_runs"],49)
        self.assertEqual(sum(sum(row["counts"].values()) for row in result["experiments"]),49)

    def test_07_greedy_temperature_invariance(self):
        torch.set_num_threads(1)
        model,tokenizer = load_baseline()
        self.assertEqual(generate(model,tokenizer,"小猫",temperature=.5)["text"],generate(model,tokenizer,"小猫",temperature=2)["text"])

    def test_08_invalid_parameters(self):
        for temp in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError): probabilities_at_temperature([2,1,0],temp)
        with self.assertRaises(ValueError): entropy([.2,.2])
        model,tokenizer = load_baseline()
        with self.assertRaises(ValueError): generate(model,tokenizer,"小猫",top_k=100)


if __name__ == "__main__": unittest.main()
