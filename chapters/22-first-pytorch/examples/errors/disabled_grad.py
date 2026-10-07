import torch
w=torch.tensor(2.,requires_grad=True)
with torch.no_grad():loss=(w*3-1)**2
loss.backward()
