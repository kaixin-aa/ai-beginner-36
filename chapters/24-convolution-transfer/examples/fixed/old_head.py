import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from conv_core import TinyCNN
model = TinyCNN(10)
model.head = torch.nn.Linear(32,2)
print(tuple(model(torch.zeros(1,1,8,8)).shape))
