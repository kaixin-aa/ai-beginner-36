"""CPU 默认；原创带少量噪声直线数据，拟合框架的最小训练循环。"""
from pathlib import Path
import numpy as np
import torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1]


def select_device(name='cpu'):
    if name not in {'cpu','cuda','auto'}:raise ValueError('设备只支持 cpu、cuda、auto')
    if name=='auto':name='cuda' if torch.cuda.is_available() else 'cpu'
    if name=='cuda' and not torch.cuda.is_available():raise ValueError('CUDA 不可用，请选择 cpu')
    return torch.device(name)


def make_data():
    rng=np.random.default_rng(42)
    x=np.linspace(-1,1,41,dtype=np.float32).reshape(-1,1)
    noise=rng.normal(0,.05,size=(41,1)).astype(np.float32)
    y=2*x+1+noise
    ids=rng.permutation(41)
    return x,y,ids[:32],ids[32:]


def autograd_demo():
    # 与第21章相同的九个初始参数，按相同的行列含义计算。
    x=torch.tensor([1.,2.],dtype=torch.float64)
    W1=torch.tensor([[.5,-1.],[1.,.5]],dtype=torch.float64,requires_grad=True)
    b1=torch.tensor([0.,-.5],dtype=torch.float64,requires_grad=True)
    W2=torch.tensor([2.,-1.],dtype=torch.float64,requires_grad=True)
    b2=torch.tensor(.5,dtype=torch.float64,requires_grad=True)
    hidden=torch.relu(x@W1+b1)
    prediction=hidden@W2+b2
    objective=(prediction-4)**2
    objective.backward()
    return {'prediction':prediction.item(),'loss':objective.item(),
            'gradients':{k:v.grad.tolist() for k,v in {'W1':W1,'b1':b1,'W2':W2,'b2':b2}.items()}}


def train_model(epochs=120,learning_rate=.1,device_name='cpu'):
    if not isinstance(epochs,int) or epochs<1:raise ValueError('训练轮数须为正整数')
    if not np.isfinite(learning_rate) or learning_rate<=0:raise ValueError('学习率须为有限正数')
    device=select_device(device_name)
    torch.manual_seed(42)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    x,y,train_ids,test_ids=make_data()
    features=torch.from_numpy(x).to(device)
    labels=torch.from_numpy(y).to(device)
    model=nn.Linear(1,1).to(device)
    loss_fn=nn.MSELoss()
    optimizer=torch.optim.SGD(model.parameters(),lr=learning_rate)
    records=[]
    model.train()
    with torch.no_grad():initial=loss_fn(model(features[train_ids]),labels[train_ids]).item()
    records.append({'epoch':0,'train_loss':initial})
    for epoch in range(1,epochs+1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        prediction=model(features[train_ids])
        objective=loss_fn(prediction,labels[train_ids])
        objective.backward()
        optimizer.step()
        with torch.no_grad():current=loss_fn(model(features[train_ids]),labels[train_ids]).item()
        records.append({'epoch':epoch,'train_loss':current})
    model.eval()
    with torch.no_grad():
        predicted=model(features).cpu().numpy()
        test_loss=loss_fn(model(features[test_ids]),labels[test_ids]).item()
        line_values=model(torch.tensor([[-1.],[0.],[1.]],device=device)).cpu().numpy().ravel().tolist()
    summary={'seed':42,'device':str(device),'torch':torch.__version__,'dtype':'float32',
             'epochs':epochs,'learning_rate':learning_rate,'batch_size':len(train_ids),'train_rows':len(train_ids),'test_rows':len(test_ids),
             'initial_train_MSE':initial,'final_train_MSE':records[-1]['train_loss'],'test_MSE':test_loss,
             'weight':model.weight.detach().cpu().item(),'bias':model.bias.detach().cpu().item(),
             'demo_inputs':[-1,0,1],'demo_predictions':line_values,'train_ids':train_ids.tolist(),'test_ids':test_ids.tolist()}
    return model,x,y,predicted,records,summary
