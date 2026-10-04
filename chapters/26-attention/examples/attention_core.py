import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_data():
    return json.loads((ROOT/"data/teaching-attention.json").read_text(encoding="utf-8"))


def softmax_rows(scores):
    scores = np.asarray(scores,dtype=np.float64)
    if scores.ndim != 2 or not scores.size or np.isnan(scores).any() or np.isposinf(scores).any():
        raise ValueError("分数须为非空二维，不能有NaN或正无穷")
    if np.isneginf(scores).all(axis=1).any():
        raise ValueError("不能把某一行的所有位置都屏蔽")
    exponential = np.exp(scores-scores.max(axis=1,keepdims=True))
    return exponential/exponential.sum(axis=1,keepdims=True)


def attention(q,k,v,causal=False):
    q,k,v = [np.asarray(a,dtype=np.float64) for a in [q,k,v]]
    if any(a.ndim != 2 or not a.size or not np.isfinite(a).all() for a in [q,k,v]):
        raise ValueError("Q、K、V须为非空有限二维矩阵")
    if q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError("Q与K特征宽度须相同，K与V位置数量须相同")
    raw = q@k.T
    scaled = raw/np.sqrt(q.shape[1])
    if causal:
        if q.shape[0] != k.shape[0]:
            raise ValueError("本章因果示例限定方形自注意力")
        scaled = np.where(np.tril(np.ones(raw.shape,dtype=bool)),scaled,-np.inf)
    weights = softmax_rows(scaled)
    output = weights@v
    return {"q":q,"k":k,"v":v,"raw":raw,"scaled":scaled,"weights":weights,"output":output}


def project_head(x,head,causal=False):
    x = np.asarray(x,dtype=np.float64)
    wq,wk,wv = [np.asarray(head[key],dtype=np.float64) for key in ["wq","wk","wv"]]
    return attention(x@wq,x@wk,x@wv,causal=causal)


def run_heads(data,causal=False):
    heads = [project_head(data["x"],head,causal) for head in data["heads"]]
    concatenated = np.concatenate([head["output"] for head in heads],axis=1)
    output = concatenated@np.asarray(data["wo"],dtype=np.float64)
    return heads,concatenated,output
