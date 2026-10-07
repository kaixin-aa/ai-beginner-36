"""从章节目录运行，保存表格、可信的本地模型和原创图。"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import hashlib
import json
import joblib
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from examples.plot_style import configure_style,new_figure,save_figure
from examples.classification_core import ROOT, BOUNDARY_FEATURES, experiment, predict_one_with_proba
from examples.project_core import TARGET_NAMES


def draw(boundary,train,test,summary):
    configure_style()
    fig,ax=new_figure('四特征模型的测试混淆矩阵','预测类别','真实类别','固定测试集 30 条；行是真实类别，列是预测类别；每格单位为条。')
    matrix=np.asarray(summary['confusion_matrix'])
    ax.grid(False)
    ax.imshow(matrix,cmap='Blues',vmin=0,vmax=10)
    ax.set_xticks(range(3),TARGET_NAMES)
    ax.set_yticks(range(3),TARGET_NAMES)
    for i in range(3):
        for j in range(3):
            ax.text(j,i,str(matrix[i,j]),ha='center',va='center',fontsize=26,color='white' if matrix[i,j]>5 else '#1c3042')
    save_figure(fig,ROOT/'assets','confusion-matrix')
    fields=BOUNDARY_FEATURES
    full=pd.concat([train,test])
    u=np.linspace(full[fields[0]].min()-.3,full[fields[0]].max()+.3,250)
    v=np.linspace(full[fields[1]].min()-.2,full[fields[1]].max()+.2,250)
    xx,yy=np.meshgrid(u,v)
    grid=pd.DataFrame(np.c_[xx.ravel(),yy.ravel()],columns=fields)
    zz=boundary.predict(grid).reshape(xx.shape)
    fig,ax=new_figure('只使用花瓣长宽的独立分类模型','花瓣长度 / 厘米','花瓣宽度 / 厘米','背景为两特征模型的预测类别；圆点为训练，三角为测试；颜色表示真实类别。')
    colors=['#2574ab','#dd8e28','#b65786']
    ax.grid(False)
    ax.contourf(xx,yy,zz,levels=[-.5,.5,1.5,2.5],cmap=ListedColormap(colors),alpha=.2)
    for label,color in enumerate(colors):
        for data,marker,size,desc in [(train,'o',32,'训练'),(test,'^',85,'测试')]:
            selected=data[data.target==label]
            ax.scatter(selected[fields[0]],selected[fields[1]],c=color,marker=marker,s=size,edgecolors='white',linewidth=.5,label=TARGET_NAMES[label]+' '+desc)
    ax.legend(fontsize=10,ncol=2,loc='upper left')
    save_figure(fig,ROOT/'assets','decision-boundary')
    wrong=test.loc[~test.correct]
    fig,ax=new_figure('两条分错样本的模型概率','模型类别','预测概率','四特征模型；柱高为模型概率，未经校准；真实标签分别为 virginica 与 versicolor。')
    positions=np.arange(3)
    for i,(_,row) in enumerate(wrong.iterrows()):
        values=[row['p_'+name] for name in TARGET_NAMES]
        ax.bar(positions+(i-.5)*.32,values,width=.32,label=row.sample_id)
    ax.set_xticks(positions,TARGET_NAMES)
    ax.set_ylim(0,1)
    ax.legend()
    save_figure(fig,ROOT/'assets','wrong-probabilities')


def main():
    model,boundary,train,test,summary=experiment()
    folder=ROOT/'results'
    folder.mkdir(exist_ok=True)
    test.to_csv(folder/'test_predictions.csv',index=False)
    pd.DataFrame(summary['confusion_matrix'],index=TARGET_NAMES,columns=TARGET_NAMES).to_csv(folder/'confusion_matrix.csv',index_label='actual')
    pd.concat([train[['sample_id','target']].assign(split='train'),test[['sample_id','target']].assign(split='test')]).to_csv(folder/'split_manifest.csv',index=False)
    joblib.dump(model,folder/'model.joblib')
    summary['model_sha256']=hashlib.sha256((folder/'model.joblib').read_bytes()).hexdigest()
    reloaded=joblib.load(folder/'model.joblib')
    np.testing.assert_allclose(reloaded.predict_proba(test[summary['features']]),model.predict_proba(test[summary['features']]))
    summary['reload_probabilities_equal']=True
    summary['single_demo']=predict_one_with_proba(reloaded,[5.1,3.5,1.4,.2])
    (folder/'classification-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    draw(boundary,train,test,summary)
    print(json.dumps({k:summary[k] for k in ['test_correct','confusion_matrix','boundary_test_accuracy','single_demo','wrong_rows']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
