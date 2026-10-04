"""以PyTorch官方缩放点积注意力独立核对NumPy无掩码与因果结果。"""
import json
import numpy as np
import torch
from attention_core import ROOT,load_data,run_heads


def main():
    errors = []
    for causal in [False,True]:
        heads,_,_ = run_heads(load_data(),causal)
        for head in heads:
            q,k,v = [torch.tensor(head[key],dtype=torch.float64)[None,None] for key in ["q","k","v"]]
            actual = torch.nn.functional.scaled_dot_product_attention(q,k,v,dropout_p=0.0,is_causal=causal)[0,0].numpy()
            np.testing.assert_allclose(actual,head["output"],atol=1e-12,rtol=1e-12)
            errors.append(float(np.max(np.abs(actual-head["output"]))))
    result = {"torch":str(torch.__version__),"dtype":"float64","device":"cpu","dropout_p":0,"cases":4,"absolute_max_errors":errors,"passed":True}
    (ROOT/"results/torch-cross-check.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
