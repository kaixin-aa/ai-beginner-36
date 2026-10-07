import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import json
from sklearn.metrics import accuracy_score
from examples.evaluation_core import binary_report,threshold_report,evaluate_existing,leakage_experiment

class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.manifests=evaluate_existing();cls.leak=leakage_experiment()
    def test_binary_hand_calculation(self):
        r=threshold_report(.5)
        self.assertEqual([r[k] for k in ['TP','FP','FN','TN']],[2,1,2,5])
        self.assertAlmostEqual(r['accuracy'],.7)
        self.assertAlmostEqual(r['precision'],2/3)
        self.assertAlmostEqual(r['recall'],.5)
        self.assertAlmostEqual(r['F1'],4/7)
    def test_lower_threshold(self):
        r=threshold_report(.25)
        self.assertEqual([r[k] for k in ['TP','FP','FN','TN']],[3,3,1,3])
        self.assertAlmostEqual(r['precision'],.5)
        self.assertAlmostEqual(r['recall'],.75)
    def test_no_positive_prediction(self):
        r=binary_report([0,1],[0,0]);self.assertEqual(r['precision'],0);self.assertEqual(r['recall'],0)
    def test_invalid_inputs(self):
        for y,p in [([],[]),([0],[0,1]),([0,2],[0,1])]:
            with self.assertRaises(ValueError):binary_report(y,p)
        with self.assertRaises(ValueError):threshold_report(float('nan'))
    def test_fold_disjoint_and_coverage(self):
        for value in self.manifests.values():
            outer=set(value['outer_train_ids']); self.assertFalse(outer&set(value['outer_test_ids']))
            seen=[]
            for fold in value['folds']:
                t=set(fold['train_positions']);v=set(fold['validation_positions'])
                self.assertFalse(t&v);self.assertEqual(t|v,set(range(len(outer))))
                seen+=fold['validation_positions']
            self.assertEqual(sorted(seen),list(range(len(outer))))
    def test_regression_historical_scores(self):
        r={x['model']:x for x in self.rows if x['task']=='regression'}
        source=Path(__file__).resolve().parents[2]/'18-linear-regression/results/regression-summary.json'
        saved=json.loads(source.read_text(encoding='utf-8'))
        self.assertAlmostEqual(r['multi']['historical_test_score'],saved['scores']['multi']['test']['MAE'],places=8)
        self.assertLess(r['multi']['cv_mean'],r['baseline']['cv_mean'])
    def test_leakage_not_random_luck(self):
        r=self.leak
        self.assertEqual(r['leaked_test_accuracy'],1)
        self.assertLess(r['clean_test_accuracy'],.65)
        self.assertEqual(r['leaked_features'],r['clean_features']+1)
        self.assertFalse(set(r['train_ids'])&set(r['test_ids']))
        self.assertAlmostEqual(r['clean_test_accuracy'],accuracy_score(r['test_labels'],r['clean_predictions']))
    def test_reproducible(self):
        self.assertEqual(self.leak,leakage_experiment())

if __name__=='__main__':unittest.main()
