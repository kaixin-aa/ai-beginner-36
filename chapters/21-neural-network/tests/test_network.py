import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from examples.network_core import X,TARGET,initial_parameters,forward,loss,gradients,update,train,numeric_gradient

class NetworkTests(unittest.TestCase):
    def test_hand_forward(self):
        f=forward(X,initial_parameters())
        np.testing.assert_allclose(f['z'],[2.5,-.5]);np.testing.assert_allclose(f['h'],[2.5,0])
        self.assertEqual(f['output'],5.5);self.assertEqual(loss(X,TARGET,initial_parameters()),2.25)
    def test_weight_change(self):
        p=initial_parameters();p['W1'][0,0]=0
        self.assertEqual(forward(X,p)['output'],4.5);self.assertEqual(loss(X,TARGET,p),.25)
    def test_gradients_by_finite_difference(self):
        p=initial_parameters();g=gradients(X,TARGET,p)
        for name,array in p.items():
            for index in np.ndindex(np.asarray(array).shape):
                self.assertAlmostEqual(float(g[name][index]),numeric_gradient(X,TARGET,p,name,index),places=6)
    def test_hand_gradient(self):
        g=gradients(X,TARGET,initial_parameters())
        np.testing.assert_allclose(g['W1'],[[6,0],[12,0]])
        np.testing.assert_allclose(g['W2'],[7.5,0]);self.assertEqual(g['b2'],3)
    def test_update_is_simultaneous_and_not_inplace(self):
        p=initial_parameters();new=update(p,gradients(X,TARGET,p))
        self.assertEqual(p['W1'][0,0],.5)
        self.assertAlmostEqual(forward(X,new)['output'],3.733)
        self.assertAlmostEqual(loss(X,TARGET,new),.071289)
    def test_activation_breakpoint(self):
        x=np.array([-2.,-1.,0.,1.,2.])
        np.testing.assert_array_equal(np.maximum(x,0)+np.maximum(-x,0),np.abs(x))
        self.assertFalse(np.isclose(np.abs(-1)+np.abs(1),2*np.abs(0)))
    def test_invalid(self):
        for x in [[1],[1,2,3],[1,float('nan')]]:
            with self.assertRaises(ValueError):forward(x,initial_parameters())
        p=initial_parameters();p['W1']=np.ones((3,2))
        with self.assertRaises(ValueError):forward(X,p)
        with self.assertRaises(ValueError):train(rate=-.1)
    def test_training_result_and_repeatability(self):
        _,r=train();_,other=train()
        self.assertEqual(r,other);self.assertEqual(len(r),21)
        self.assertLess(r[-1]['loss'],1e-10)

if __name__=='__main__':unittest.main()
