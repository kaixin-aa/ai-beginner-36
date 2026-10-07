import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from examples.torch_core import make_data,train_model,autograd_demo,select_device

class TorchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.model,cls.x,cls.y,cls.pred,cls.records,cls.summary=train_model()
    def test_data_and_shapes(self):
        x,y,t,v=make_data();self.assertEqual(x.shape,(41,1));self.assertEqual(y.shape,(41,1))
        self.assertFalse(set(t)&set(v));self.assertEqual(sorted(t.tolist()+v.tolist()),list(range(41)))
    def test_manual_gradient(self):
        r=autograd_demo();self.assertEqual(r['prediction'],5.5);self.assertEqual(r['loss'],2.25)
        np.testing.assert_allclose(r['gradients']['W1'],[[6,0],[12,0]])
        np.testing.assert_allclose(r['gradients']['b1'],[6,0])
        np.testing.assert_allclose(r['gradients']['W2'],[7.5,0]);self.assertEqual(r['gradients']['b2'],3)
    def test_fit_and_metric_independent(self):
        s=self.summary;self.assertLess(s['final_train_MSE'],.005)
        self.assertLess(s['test_MSE'],.01)
        self.assertAlmostEqual(s['test_MSE'],float(np.mean((self.y[s['test_ids']]-self.pred[s['test_ids']])**2)),places=7)
        self.assertAlmostEqual(s['weight'],2,delta=.08);self.assertAlmostEqual(s['bias'],1,delta=.05)
    def test_test_labels_do_not_participate(self):
        # 独立手算一轮 SGD，与程序第一轮损失比较，输入仅用训练位置。
        torch.manual_seed(42);model=torch.nn.Linear(1,1)
        x,y,t,_=make_data();weight=model.weight.item();bias=model.bias.item()
        residual=x[t]*weight+bias-y[t]
        next_w=weight-.1*float(2*np.mean(residual*x[t]));next_b=bias-.1*float(2*residual.mean())
        mse=float(np.mean((x[t]*next_w+next_b-y[t])**2))
        self.assertAlmostEqual(mse,self.records[1]['train_loss'],places=6)
    def test_reproducibility(self):
        *_,records,summary=train_model()
        self.assertEqual(self.records,records);self.assertEqual(self.summary,summary)
    def test_mode_and_grad_differ(self):
        module=torch.nn.Dropout(.5);x=torch.ones(20)
        module.eval();torch.testing.assert_close(module(x),x)
        layer=torch.nn.Linear(1,1);layer.eval()
        self.assertTrue(layer(torch.ones(1,1)).requires_grad)
        with torch.no_grad():self.assertFalse(layer(torch.ones(1,1)).requires_grad)
    def test_gradient_accumulation(self):
        w=torch.tensor(2.,requires_grad=True)
        (w*3-1).square().backward();self.assertEqual(w.grad.item(),30)
        (w*3-1).square().backward();self.assertEqual(w.grad.item(),60)
        w.grad=None;(w*3-1).square().backward();self.assertEqual(w.grad.item(),30)
    def test_shared_memory(self):
        array=np.array([1.,2.],dtype=np.float32);tensor=torch.from_numpy(array);tensor[0]=9
        self.assertEqual(array[0],9)
        clone=tensor.clone();clone[0]=3;self.assertEqual(array[0],9)
    def test_device_and_invalid(self):
        self.assertEqual(str(select_device('cpu')),'cpu')
        with self.assertRaises(ValueError):select_device('other')
        with self.assertRaises(ValueError):train_model(epochs=0)
        with self.assertRaises(ValueError):train_model(learning_rate=float('nan'))

if __name__=='__main__':unittest.main()
