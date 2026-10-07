import hashlib
import json
from pathlib import Path
import sys
import torch
from torch.nn import functional as F

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = ROOT.parent/"27-transformer/examples"
sys.path.insert(0,str(DEPENDENCY))
from toy_transformer import load_model,generate,make_batch


def load_teaching():
    return json.loads((ROOT/"data/teaching-stages.json").read_text(encoding="utf-8"))


def probabilities_at_temperature(logits,temperature):
    values = torch.as_tensor(logits,dtype=torch.float64)
    if values.ndim!=1 or not len(values) or not torch.isfinite(values).all() or not 0<temperature<float("inf"):
        raise ValueError("需要有限一维分数和有限正温度")
    return torch.softmax(values/temperature,dim=0)


def entropy(probabilities):
    p = torch.as_tensor(probabilities,dtype=torch.float64)
    if (p<0).any() or not torch.isclose(p.sum(),torch.tensor(1.,dtype=torch.float64)):
        raise ValueError("需要非负且和为1的分配")
    p = p[p>0]
    return float(-(p*p.log()).sum())


def response_only_mask(tokenizer,prompt,response):
    ids = tokenizer.encode(prompt+response,bos=True,eos=True)
    x = torch.tensor([ids[:-1]],dtype=torch.long)
    y = torch.tensor([ids[1:]],dtype=torch.long)
    # 输入第len(prompt)位置开始预测回复第一字；此前位置预测提示文字，排除。
    y[:,:len(tokenizer.encode(prompt))] = -100
    return x,y


def model_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_baseline():
    metadata = json.loads((ROOT/"data/baseline-metadata.json").read_text(encoding="utf-8"))
    path = ROOT/"data/fixed-transformer.pt"
    if model_sha(path)!=metadata["sha256"]:
        raise ValueError("固定模型快照哈希不一致")
    return load_model(path)
