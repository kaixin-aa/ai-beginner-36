import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from examples.classification_core import experiment,predict_one_with_proba,probability_result,BOUNDARY_FEATURES
from examples.project_core import FEATURES

class ClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model,cls.boundary,cls.train,cls.test,cls.summary=experiment()
    def test_split_counts_and_ids(self):
        self.assertEqual(self.summary['all_class_counts'],[50,50,50])
        self.assertEqual(self.summary['train_class_counts'],[40,40,40])
        self.assertEqual(self.summary['test_class_counts'],[10,10,10])
        self.assertFalse(set(self.train.sample_id)&set(self.test.sample_id))
    def test_scaler_training_only(self):
        scaler=self.model.named_steps['scale']
        self.assertEqual(scaler.n_samples_seen_,120)
        np.testing.assert_allclose(scaler.mean_,self.train[FEATURES].mean())
    def test_probability_and_predict(self):
        labels,p,classes=probability_result(self.model,self.test[FEATURES])
        np.testing.assert_allclose(p.sum(axis=1),1)
        np.testing.assert_array_equal(labels,self.model.predict(self.test[FEATURES]))
    def test_matrix_independent(self):
        actual=np.zeros((3,3),dtype=int)
        for y,p in zip(self.test.target,self.test.prediction):
            actual[int(y),int(p)]+=1
        self.assertEqual(actual.tolist(),self.summary['confusion_matrix'])
        self.assertEqual(int(actual.trace()),self.summary['test_correct'])
    def test_class_order(self):
        class Fake:
            classes_=np.array([2,0,1])
            def predict_proba(self,x): return np.tile([.7,.2,.1],(len(x),1))
        labels,_,_=probability_result(Fake(),pd.DataFrame([[1]]))
        self.assertEqual(labels.tolist(),[2])
    def test_invalid_inputs(self):
        for values in [[1,2,3],[1,2,3,4,5],[1,2,3,float('nan')],[1,2,3,0],{'target':0}]:
            with self.assertRaises(ValueError):predict_one_with_proba(self.model,values)
    def test_single_and_batch(self):
        row=self.test.iloc[0][FEATURES].to_dict()
        result=predict_one_with_proba(self.model,row)
        self.assertEqual(result['label'],int(self.test.iloc[0].prediction))
        self.assertAlmostEqual(sum(result['probabilities'].values()),1)
    def test_two_features_separate(self):
        self.assertEqual(self.boundary.n_features_in_,2)
        self.assertEqual(self.model.n_features_in_,4)
        self.assertEqual(BOUNDARY_FEATURES,FEATURES[2:])

if __name__=='__main__':unittest.main()
