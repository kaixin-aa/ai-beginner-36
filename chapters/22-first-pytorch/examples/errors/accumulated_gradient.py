import torch
w=torch.tensor(2.,requires_grad=True)
for _ in range(2):(w*3-1).square().backward()
print('梯度',w.grad.item())
assert w.grad.item()==30,'前一轮梯度没有清除'
