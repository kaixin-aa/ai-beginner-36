import torch
w=torch.tensor(2.,requires_grad=True)
loss=(w*3-1)**2
loss.backward()
print('损失',loss.item(),'梯度',w.grad.item())
