"""错误示例，十类源头没有换成二类目标头。"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from conv_core import TinyCNN
output = TinyCNN(10)(torch.zeros(1,1,8,8))
assert output.shape[1] == 2, "目标只有even和odd，必须替换十类源分类头"
