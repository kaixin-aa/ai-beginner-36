import torch
w=torch.tensor(2.,requires_grad=True)
for _ in range(2):
    w.grad=None
    (w*3-1).square().backward()
print('每轮清除后的梯度',w.grad.item())
assert w.grad.item()==30
