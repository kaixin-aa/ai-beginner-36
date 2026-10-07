import numpy as np
x=np.array([1.,2.]);weights=np.array([[.5,-1.],[1.,.5]])
wrong=x*weights
print(wrong)
assert wrong.shape==(2,),'逐元素乘法没有计算每个隐藏节点的加权和'
