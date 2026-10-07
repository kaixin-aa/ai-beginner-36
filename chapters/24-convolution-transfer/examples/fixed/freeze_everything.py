import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from conv_core import TinyCNN, freeze_features
model = TinyCNN(2)
freeze_features(model)
loss = torch.nn.CrossEntropyLoss()(model(torch.zeros(1,1,8,8)),torch.tensor([0]))
loss.backward()
print("特征梯度为空",all(p.grad is None for p in model.features.parameters()))
print("新分类头有梯度",all(p.grad is not None for p in model.head.parameters()))
