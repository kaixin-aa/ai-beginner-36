import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse,csv,json,time
import numpy as np
import torch
from examples.torch_core import ROOT,train_model,autograd_demo
from examples.plot_style import configure_style,new_figure,save_figure


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--device',default='cpu',choices=['cpu','cuda','auto'])
    args=parser.parse_args()
    started=time.perf_counter()
    model,x,y,predicted,records,summary=train_model(device_name=args.device)
    elapsed=time.perf_counter()-started
    summary['training_elapsed_seconds']=elapsed
    summary['autograd_demo']=autograd_demo()
    model=model.cpu()
    folder=ROOT/'results';folder.mkdir(exist_ok=True)
    torch.save(model.state_dict(),folder/'linear-state.pt')
    reloaded=torch.nn.Linear(1,1)
    reloaded.load_state_dict(torch.load(folder/'linear-state.pt',map_location='cpu',weights_only=True));reloaded.eval()
    with torch.no_grad():np.testing.assert_allclose(reloaded(torch.from_numpy(x)).numpy(),predicted,rtol=1e-5,atol=1e-6)
    summary['reload_predictions_equal']=True
    (folder/'training-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (folder/'loss_history.csv').open('w',newline='',encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=records[0]);writer.writeheader();writer.writerows(records)
    with (ROOT/'data/teaching_line.csv').open('w',newline='',encoding='utf-8') as file:
        writer=csv.writer(file);writer.writerow(['sample_id','x','y','split','prediction'])
        train_ids=set(summary['train_ids'])
        for i in range(len(x)):writer.writerow([i,float(x[i,0]),float(y[i,0]),'train' if i in train_ids else 'test',float(predicted[i,0])])
    configure_style()
    fig,ax=new_figure('PyTorch CPU 训练的平方损失','已完成训练轮数','训练 MSE / 教学数值','原创直线加噪声；每轮使用全部 32 条训练记录；第零轮为更新前损失。')
    ax.plot([r['epoch'] for r in records],[r['train_loss'] for r in records],lw=2)
    ax.set_ylim(bottom=0);save_figure(fig,ROOT/'assets','training-loss')
    fig,ax=new_figure('拟合一组原创直线数据','输入 x / 教学数值','目标与预测 y / 教学数值','生成关系 y = 2x + 1 + 噪声；固定划分 32/9；本章只评估同一生成范围内的小型实验。')
    for split,ids,color in [('训练',summary['train_ids'],'#4181b0'),('测试',summary['test_ids'],'#c78447')]:
        ax.scatter(x[ids,0],y[ids,0],label=split+'真实值',color=color,s=55)
    ax.plot(x[:,0],predicted[:,0],label='模型预测',color='#608a56',lw=2.5)
    ax.legend(fontsize=13);save_figure(fig,ROOT/'assets','fitted-line')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
