"""全为原创教学数字；输入一条二维记录，隐藏层两个节点，输出一个数值。"""
import numpy as np

X=np.array([1.,2.]);TARGET=4.

def initial_parameters():
    return {'W1':np.array([[.5,-1.],[1.,.5]]),'b1':np.array([0.,-.5]),'W2':np.array([2.,-1.]),'b2':np.array(.5)}

def validate(x,p):
    x=np.asarray(x,dtype=float)
    if x.shape!=(2,) or not np.isfinite(x).all():raise ValueError('本章输入需要两个有限数值')
    expected={'W1':(2,2),'b1':(2,),'W2':(2,),'b2':()}
    if set(p)!=set(expected):raise ValueError('参数字段不全或多余')
    for name,shape in expected.items():
        if np.asarray(p[name]).shape!=shape or not np.isfinite(p[name]).all():raise ValueError('参数形状或数值错误 '+name)
    return x

def forward(x,p):
    x=validate(x,p)
    z=x@p['W1']+p['b1']
    h=np.maximum(0,z)
    output=float(h@p['W2']+p['b2'])
    return {'z':z,'h':h,'output':output}

def loss(x,target,p):
    if not np.isfinite(target):raise ValueError('目标值须有限')
    return float((forward(x,p)['output']-target)**2)

def gradients(x,target,p):
    values=forward(x,p)
    if not np.isfinite(target):raise ValueError('目标值须有限')
    # 反向按计算链求梯度，ReLU 在零处采用零次梯度约定。
    delta=2*(values['output']-target)
    dz=delta*p['W2']*(values['z']>0)
    return {'W1':np.outer(np.asarray(x),dz),'b1':dz,'W2':delta*values['h'],'b2':np.array(delta)}

def update(p,g,rate=.02):
    if not np.isfinite(rate) or rate<=0:raise ValueError('学习率须为有限正数')
    return {name:np.asarray(p[name])-rate*g[name] for name in p}

def train(steps=20,rate=.02):
    if not isinstance(steps,int) or steps<0:raise ValueError('更新次数须为非负整数')
    p=initial_parameters();records=[]
    for step in range(steps+1):
        f=forward(X,p)
        records.append({'step':step,'prediction':f['output'],'loss':loss(X,TARGET,p),'z1':float(f['z'][0]),'z2':float(f['z'][1])})
        if step<steps:p=update(p,gradients(X,TARGET,p),rate)
    return p,records

def numeric_gradient(x,target,p,name,index,epsilon=1e-6):
    plus={k:np.array(v,copy=True) for k,v in p.items()};minus={k:np.array(v,copy=True) for k,v in p.items()}
    plus[name][index]+=epsilon;minus[name][index]-=epsilon
    return (loss(x,target,plus)-loss(x,target,minus))/(2*epsilon)
