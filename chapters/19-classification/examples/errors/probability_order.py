import numpy as np
classes=np.array([2,0,1])
p=np.array([.7,.2,.1])
wrong=int(p.argmax())
assert wrong==classes[p.argmax()], '最大概率的位置不能当成类别编码'
