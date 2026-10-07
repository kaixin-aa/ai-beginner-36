import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json
import pandas as pd
import numpy as np
from examples.evaluation_core import ROOT,evaluate_existing,leakage_experiment,threshold_report,SPAM_Y,SPAM_P,binary_report
from examples.plot_style import configure_style,new_figure,save_figure


def main():
    configure_style()
    rows,manifest=evaluate_existing()
    leak=leakage_experiment()
    threshold=[threshold_report(.5),threshold_report(.25)]
    majority=binary_report(np.array([0]*95+[1]*5),np.zeros(100,dtype=int))
    out=ROOT/'results'; out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'model_comparison.csv',index=False)
    pd.DataFrame(threshold).to_csv(out/'threshold_comparison.csv',index=False)
    pd.DataFrame({'true_label':SPAM_Y,'model_probability':SPAM_P,'prediction_050':(SPAM_P>=.5).astype(int),'prediction_025':(SPAM_P>=.25).astype(int)}).to_csv(out/'teaching_spam.csv',index=False)
    summary={'date':'2026-10-03','models':rows,'thresholds':threshold,'majority_baseline':majority,
        'leakage':leak,'cv_seed':7,'folds':5,'test_role':'复用过的历史测试集，仅作教学复核，不声称新独立评估'}
    for name,value in [('evaluation-summary.json',summary),('fold_manifest.json',manifest)]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fig,ax=new_figure('同一批训练数据内的五折分类评估','模型','准确率','每折 96 条训练、24 条验证；误差线为五折标准差，未解释成置信区间。')
    chosen=[row for row in rows if row['task']=='classification']
    positions=np.arange(len(chosen))
    ax.bar(positions-.18,[r['train_score'] for r in chosen],width=.36,label='全训练部分得分',color='#6b94bb')
    ax.bar(positions+.18,[r['cv_mean'] for r in chosen],yerr=[r['cv_std'] for r in chosen],capsize=4,width=.36,label='折内验证均值',color='#c78447')
    ax.set_xticks(positions,['多数类基线','逻辑回归','一层树','完整树']); ax.set_ylim(0,1.12);ax.legend(fontsize=13)
    save_figure(fig,ROOT/'assets','overfitting-comparison')
    fig,ax=new_figure('复制标签制造的虚假满分','实验流程','准确率','400 条原创随机数据；固定划分 300/100；泄漏列是答案，实际预测时无法获得。')
    positions=np.arange(2)
    ax.bar(positions-.18,[leak['clean_train_accuracy'],leak['leaked_train_accuracy']],width=.36,label='训练',color='#6b94bb')
    ax.bar(positions+.18,[leak['clean_test_accuracy'],leak['leaked_test_accuracy']],width=.36,label='测试',color='#c78447')
    ax.set_xticks(positions,['仅六列噪声','噪声加答案列']);ax.set_ylim(0,1.12);ax.legend()
    for i,value in enumerate([leak['clean_test_accuracy'],leak['leaked_test_accuracy']]):ax.text(i+.18,value+.025,f'{value:.2f}',ha='center')
    save_figure(fig,ROOT/'assets','leakage-demo')
    print(json.dumps({'models':rows,'thresholds':threshold,'leakage':{k:v for k,v in leak.items() if not isinstance(v,list)}},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
