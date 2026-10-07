"""错误示例，将新分类头也冻结后，损失无参数梯度。"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from conv_core import TinyCNN
model = TinyCNN(2)
for p in model.parameters():
    p.requires_grad_(False)
loss = torch.nn.CrossEntropyLoss()(model(torch.zeros(1,1,8,8)),torch.tensor([0]))
loss.backward()
