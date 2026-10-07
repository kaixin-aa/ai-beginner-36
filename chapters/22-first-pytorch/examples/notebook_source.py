CELLS=[
('markdown','# 第 22 章首次 PyTorch\n全部直线数据为原创教学设定。固定 CPU、种子 42、120 轮，主程序先生成图。'),
('code','import torch,numpy as np\nprint("PyTorch",torch.__version__)\narray=np.array([1.,2.],dtype=np.float32)\ntensor=torch.from_numpy(array)\ntensor[0]=9\nprint("共享",array)\nprint("形状/类型/设备",tensor.shape,tensor.dtype,tensor.device)'),
('code','from examples.torch_core import autograd_demo\nprint(autograd_demo())'),
('code','from examples.torch_core import train_model\nmodel,x,y,predicted,records,summary=train_model()\nprint({k:v for k,v in summary.items() if not isinstance(v,list)})'),
('code','print("首轮",records[1])\nprint("末轮",records[-1])\nprint("-1/0/1 预测",summary["demo_predictions"])'),
('code','layer=torch.nn.Linear(1,1)\nlayer.eval()\nprint("eval仍求导",layer(torch.ones(1,1)).requires_grad)\nwith torch.no_grad():\n    print("no_grad关闭求导",layer(torch.ones(1,1)).requires_grad)'),
('code','w=torch.tensor(2.,requires_grad=True)\nfor _ in range(2):\n    (w*3-1).square().backward()\nprint("累计梯度",w.grad.item())\nw.grad=None\n(w*3-1).square().backward()\nprint("清除后",w.grad.item())'),
('code','from IPython.display import display,Image\nfor name in ["training-loss","fitted-line"]:\n    display(Image(filename=f"assets/{name}.png",width=700))'),
]
