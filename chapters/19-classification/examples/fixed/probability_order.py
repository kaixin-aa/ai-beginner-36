import numpy as np
classes=np.array([2,0,1])
p=np.array([.7,.2,.1])
label=int(classes[p.argmax()])
assert label==2
print('类别',label,'概率',p.max())
