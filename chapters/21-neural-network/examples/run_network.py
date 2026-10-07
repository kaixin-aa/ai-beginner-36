import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import csv,json
import numpy as np
from matplotlib.patches import Circle,FancyArrowPatch
from examples.network_core import X,TARGET,initial_parameters,forward,loss,gradients,update,train,numeric_gradient
from examples.plot_style import configure_style,new_figure,save_figure
ROOT=Path(__file__).resolve().parents[1]


def draw(records):
    configure_style()
    fig,ax=new_figure('二维输入到双节点隐藏层再到单个输出','','','原创教学网络；W1 行对应输入、列对应隐藏节点；输出为数值，无分类概率含义。')
    ax.set_axis_off();ax.set_xlim(-.1,1.1);ax.set_ylim(0,1)
    positions=[(.04,.7),(.04,.3),(.49,.7),(.49,.3),(.94,.5)]
    edges=[(0,2,'0.5',.42),(1,2,'1.0',.32),(0,3,'−1.0',.32),(1,3,'0.5',.42),(2,4,'2.0',.4),(3,4,'−1.0',.4)]
    for start,end,weight,t in edges:
        a=np.array(positions[start]);b=np.array(positions[end])
        direction=(b-a)/np.linalg.norm(b-a)
        ax.add_patch(FancyArrowPatch(a+direction*.065,b-direction*.065,arrowstyle='-|>',mutation_scale=15,color='#7892a6',lw=1.8))
        where=a+t*(b-a)
        ax.text(*where,weight,ha='center',va='center',fontsize=13,bbox={'facecolor':'white','edgecolor':'none','pad':1})
    texts=['x1 = 1','x2 = 2','h1 = 2.5','h2 = 0','输出 5.5']
    for pos,text in zip(positions,texts):
        ax.add_patch(Circle(pos,.066,facecolor='#e5eef6',edgecolor='#32688e',lw=1.5))
        ax.text(*pos,text,ha='center',va='center',fontsize=13)
    ax.text(.04,.91,'输入 shape (2,)',ha='center',fontsize=15)
    ax.text(.49,.91,'隐藏 shape (2,)\nz = x @ W1 + b1，h = ReLU(z)',ha='center',fontsize=14)
    ax.text(.94,.91,'标量输出',ha='center',fontsize=15)
    ax.text(.49,.08,'b1 = [0, −0.5]',ha='center',fontsize=15)
    ax.text(.94,.08,'b2 = 0.5',ha='center',fontsize=15)
    save_figure(fig,ROOT/'assets','network-structure')
    xx=np.linspace(-2,2,201)
    fig,ax=new_figure('激活函数让组合计算出现折点','输入 x / 教学数值','输出 / 教学数值','隐藏节点为 ReLU(x) 与 ReLU(−x)；两项相加得到 |x|；移除 ReLU 后输出恒为零。')
    ax.plot(xx,np.maximum(xx,0)+np.maximum(-xx,0),label='加入 ReLU',lw=3)
    ax.plot(xx,xx+(-xx),label='移除 ReLU',lw=3,linestyle=':')
    ax.legend(fontsize=13);save_figure(fig,ROOT/'assets','activation-effect')
    fig,ax=new_figure('同一条教学样本的二十次参数更新','已完成更新次数','平方损失 / 教学数值','目标值为 4；学习率 0.02；仅演示拟合一条样本，不评估未知数据能力。')
    ax.plot([r['step'] for r in records],[r['loss'] for r in records],marker='o',lw=2)
    ax.set_ylim(bottom=0);save_figure(fig,ROOT/'assets','loss-updates')


def main():
    p=initial_parameters();f=forward(X,p);g=gradients(X,TARGET,p)
    altered=initial_parameters();altered['W1'][0,0]=0
    next_p=update(p,g)
    final,records=train()
    out=ROOT/'results';out.mkdir(exist_ok=True)
    with (out/'updates.csv').open('w',newline='',encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=records[0].keys());writer.writeheader();writer.writerows(records)
    hand=[{'quantity':'z1','calculation':'1*0.5+2*1+0','value':float(f['z'][0])},
          {'quantity':'z2','calculation':'1*(-1)+2*0.5-0.5','value':float(f['z'][1])},
          {'quantity':'h1','calculation':'max(0,z1)','value':float(f['h'][0])},
          {'quantity':'h2','calculation':'max(0,z2)','value':float(f['h'][1])},
          {'quantity':'prediction','calculation':'h1*2+h2*(-1)+0.5','value':f['output']},
          {'quantity':'loss','calculation':'(prediction-4)**2','value':loss(X,TARGET,p)}]
    with (out/'hand_calculation.csv').open('w',newline='',encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=hand[0].keys());writer.writeheader();writer.writerows(hand)
    comparisons=[]
    for name,array in p.items():
        for index in np.ndindex(np.asarray(array).shape):
            comparisons.append({'parameter':name,'index':list(index),'analytic':float(g[name][index]),'numeric':float(numeric_gradient(X,TARGET,p,name,index))})
    summary={'source':'全部网络输入、权重和目标为原创教学设定','initial':{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in f.items()},
        'initial_loss':loss(X,TARGET,p),'changed_weight_prediction':forward(X,altered)['output'],
        'changed_weight_loss':loss(X,TARGET,altered),'gradients':{k:v.tolist() for k,v in g.items()},
        'one_update_parameters':{k:v.tolist() for k,v in next_p.items()},'one_update':records[1],
        'last_update':records[-1],'gradient_comparison':comparisons,'learning_rate':.02,'steps':20}
    (out/'network-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    draw(records)
    print(json.dumps({k:v for k,v in summary.items() if k!='gradient_comparison'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
