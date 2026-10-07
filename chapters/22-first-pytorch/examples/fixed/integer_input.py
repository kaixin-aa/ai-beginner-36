import torch
model=torch.nn.Linear(1,1)
with torch.no_grad():
    model.weight.fill_(2);model.bias.fill_(1)
x=torch.tensor([[1],[2]],dtype=torch.float32)
print(model(x).detach())
