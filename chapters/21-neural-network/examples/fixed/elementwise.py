import numpy as np
x=np.array([1.,2.]);weights=np.array([[.5,-1.],[1.,.5]])
z=x@weights+np.array([0.,-.5])
print('形状',z.shape,'结果',z)
assert z.shape==(2,)
