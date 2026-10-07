import math
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"examples"))
from attention_core import *


class Chapter26Tests(unittest.TestCase):
    def test_01_projection_and_shapes(self):
        data = load_data()
        heads,concat,out = run_heads(data)
        for head in heads:
            for key in ["q","k","v","output"]: self.assertEqual(head[key].shape,(4,2))
            self.assertEqual(head["weights"].shape,(4,4))
        self.assertEqual(concat.shape,(4,4))
        self.assertEqual(out.shape,(4,4))
        np.testing.assert_array_equal(heads[0]["q"],data["heads"][0]["wq"])

    def test_02_independent_pronoun_hand_calculation(self):
        head = run_heads(load_data())[0][0]
        np.testing.assert_array_equal(head["raw"][2],[4,0,0,2])
        values = [math.exp(4/math.sqrt(2)),1,1,math.exp(2/math.sqrt(2))]
        expected = np.array(values)/sum(values)
        np.testing.assert_allclose(head["weights"][2],expected,atol=1e-14)
        np.testing.assert_allclose(head["output"][2],[expected[0]+expected[3],expected[1]+expected[3]])

    def test_03_row_sums_and_nonnegative(self):
        for head in run_heads(load_data())[0]:
            np.testing.assert_allclose(head["weights"].sum(axis=1),np.ones(4))
            self.assertTrue((head["weights"]>=0).all())

    def test_04_stable_softmax_offset_invariance(self):
        a = softmax_rows([[1,2,3]])
        b = softmax_rows([[10001,10002,10003]])
        np.testing.assert_allclose(a,b)
        np.testing.assert_allclose(softmax_rows([[0,0,0]]),[[1/3]*3])

    def test_05_mask(self):
        heads,_,_ = run_heads(load_data(),True)
        for head in heads:
            self.assertEqual(np.count_nonzero(np.triu(head["weights"],1)),0)
            np.testing.assert_allclose(head["weights"].sum(1),1)
            np.testing.assert_allclose(head["output"][0],head["v"][0])

    def test_06_v_changes_output_but_not_weights(self):
        head = run_heads(load_data())[0][0]
        changed = attention(head["q"],head["k"],head["v"]*2)
        np.testing.assert_array_equal(changed["weights"],head["weights"])
        np.testing.assert_allclose(changed["output"],2*head["output"])

    def test_07_different_heads(self):
        heads,concat,out = run_heads(load_data())
        self.assertEqual(heads[0]["weights"][2].argmax(),0)
        self.assertEqual(heads[1]["weights"][2].argmax(),3)
        np.testing.assert_array_equal(concat[:,:2],heads[0]["output"])

    def test_08_permutation_without_positions(self):
        head = run_heads(load_data())[0][0]
        order = [2,0,3,1]
        shuffled = attention(head["q"][order],head["k"][order],head["v"][order])
        np.testing.assert_allclose(shuffled["output"],head["output"][order])

    def test_09_invalid_shape_and_all_masked_row(self):
        with self.assertRaises(ValueError): attention(np.ones((4,2)),np.ones((4,3)),np.ones((4,2)))
        with self.assertRaises(ValueError): softmax_rows([[-np.inf,-np.inf]])
        with self.assertRaises(ValueError): softmax_rows([[np.inf,0]])


if __name__ == "__main__": unittest.main()
