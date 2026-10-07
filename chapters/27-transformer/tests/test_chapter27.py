import sys
from pathlib import Path
import unittest
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"examples"))
from toy_transformer import *


class Chapter27Tests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        torch.manual_seed(42)
        self.tokenizer = CharacterTokenizer.from_sentences(load_corpus()["sentences"])
        self.model = TinyTransformer(len(self.tokenizer.tokens),**CONFIG).eval()

    def test_01_tokenizer_and_padding(self):
        for text in load_corpus()["sentences"]:
            self.assertEqual(self.tokenizer.decode(self.tokenizer.encode(text,bos=True,eos=True)),text)
        x,y = make_batch(["我读书。","小猫吃鱼。"],self.tokenizer)
        self.assertEqual(int(y[0,-1]),-100)
        self.assertEqual(int(x[0,0]),self.tokenizer.bos)
        self.assertEqual(int(y[1,-1]),self.tokenizer.eos)

    def test_02_causal_future_invariance(self):
        a = torch.tensor([self.tokenizer.encode("小猫吃鱼",bos=True)])
        b = torch.tensor([self.tokenizer.encode("小猫喝水",bos=True)])
        with torch.no_grad():
            left,right = self.model(a),self.model(b)
        torch.testing.assert_close(left[:,:3],right[:,:3],atol=1e-6,rtol=1e-6)

    def test_03_shapes_and_position_embedding(self):
        x = torch.tensor([[self.tokenizer.ids["小"]]*3])
        _,shapes = self.model(x,True)
        self.assertEqual(shapes["qkv_each"],[1,2,3,8])
        self.assertEqual(shapes["ff_hidden"],[1,3,32])
        self.assertFalse(torch.equal(self.model.position_embedding.weight[0],self.model.position_embedding.weight[1]))

    def test_04_layernorm_independent_formula(self):
        values = torch.tensor([[1.,2.,3.,4.]])
        actual = nn.LayerNorm(4,elementwise_affine=False,eps=1e-5)(values)
        expected = (values-2.5)/torch.sqrt(torch.tensor(1.25+1e-5))
        torch.testing.assert_close(actual,expected)

    def test_05_residual_zero_branches_preserve_input(self):
        for module in [self.model.attention_out,self.model.feed_forward[2]]:
            nn.init.zeros_(module.weight)
            nn.init.zeros_(module.bias)
        ids = torch.tensor([[1,3,4]])
        embedded = self.model.token_embedding(ids)+self.model.position_embedding(torch.arange(3))[None]
        expected = self.model.language_head(self.model.final_norm(embedded))
        torch.testing.assert_close(self.model(ids),expected)

    def test_06_saved_model_generation_and_limits(self):
        model,tokenizer = load_model(ROOT/"results/tiny-transformer.pt")
        a,b = generate(model,tokenizer,"小猫"),generate(model,tokenizer,"小猫")
        self.assertEqual(a,b)
        self.assertEqual(a["stop_reason"],"eos")
        self.assertTrue(a["text"].startswith("小猫"))
        self.assertEqual(a["trace"][-1]["selected_token"],"<EOS>")
        limited = generate(model,tokenizer,"小猫",max_new_tokens=1)
        self.assertEqual(len(limited["trace"]),1)
        self.assertEqual(limited["stop_reason"],"max_new_tokens")

    def test_07_loss_mask_independent(self):
        scores = torch.tensor([[1.,0.],[0.,1.]])
        target = torch.tensor([0,-100])
        loss = F.cross_entropy(scores,target,ignore_index=-100)
        expected = -torch.log_softmax(scores[0],0)[0]
        torch.testing.assert_close(loss,expected)

    def test_08_saved_summary_matches_actual(self):
        summary = json.loads((ROOT/"results/transformer-summary.json").read_text(encoding="utf-8"))
        self.assertTrue(summary["reload_logits_identical"])
        self.assertFalse(summary["independent_test"])
        self.assertLess(summary["final_train_loss"],summary["initial_train_loss"])
        model,_ = load_model(ROOT/"results/tiny-transformer.pt")
        self.assertEqual(summary["parameters"],sum(p.numel() for p in model.parameters()))

    def test_09_invalid_inputs(self):
        with self.assertRaises(ValueError): self.tokenizer.encode("火星")
        with self.assertRaises(ValueError): self.model(torch.zeros(1,17,dtype=torch.long))
        with self.assertRaises(ValueError): self.model(torch.ones(1,3))
        with self.assertRaises(ValueError): generate(self.model,self.tokenizer,"小猫",temperature=0)


if __name__ == "__main__": unittest.main()
