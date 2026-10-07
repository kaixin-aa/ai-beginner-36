import numpy as np
x=np.array([1.,2.]);weights=np.array([[.5,-1.],[1.,.5]])
print(x@weights+np.array([0.,-.5]))
