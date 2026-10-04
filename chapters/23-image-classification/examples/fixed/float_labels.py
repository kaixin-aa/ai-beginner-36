import torch
from torch import nn

logits = torch.tensor([[1.0, 0.0, -1.0]])
labels = torch.tensor([0], dtype=torch.long)
print("交叉熵", round(nn.CrossEntropyLoss()(logits, labels).item(), 6))
