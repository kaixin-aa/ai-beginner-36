import torch
model=torch.nn.Linear(1,1)
x=torch.tensor([[1],[2]])
print(model(x))
