import json
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure,new_figure
ROOT=Path(__file__).resolve().parents[1]


def draw():
    configure_style()
    fig,ax=plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.04,right=.96,top=.85,bottom=.17)
    ax.axis("off");ax.set(xlim=(0,1),ylim=(0,1))
    fig.suptitle("先检索资料，再把片段交给模型",fontsize=23,y=.94)
    labels=["本地文档\n文件和行号","切分与编码\n512维单位向量","保存索引\nJSON 与 NPY","问题检索\n门槛及前3项","生成与核对\n来源和原文"]
    for i,label in enumerate(labels):
        x=.015+i*.2
        ax.add_patch(FancyBboxPatch((x,.55),.165,.26,boxstyle="round,pad=.006",facecolor="#eaf2ff" if i<3 else "#e0f1ec",edgecolor="#8296aa"))
        ax.text(x+.0825,.68,label,ha="center",va="center",fontsize=13,linespacing=1.7)
        if i<4:ax.annotate("",xy=(x+.193,.68),xytext=(x+.173,.68),arrowprops={"arrowstyle":"->","lw":1.7})
    ax.text(.5,.35,"查无片段直接说明；资料有冲突则引用双方",ha="center",fontsize=17)
    ax.text(.5,.18,"检索分数不等于正确概率，引用对应也不等于推理必然正确",ha="center",fontsize=14,color="#536275")
    fig.text(.05,.06,"原创教学图   Embedding 在本机运行，生成仅发送选中的原创资料片段",fontsize=13,color="#536275")
    save_figure(fig,ROOT/"assets","rag-flow")
    records=json.loads((ROOT/"results/retrieval-results.json").read_text(encoding="utf-8"))["records"]
    chosen=[records[i]for i in (0,1,5,6,7)]
    values=[max(item["all_scores"])for item in chosen]
    fig,ax=new_figure("相似度高，资料仍可能没有所问事实","问题类型","最高余弦相似度","真实公开模型编码   教学门槛0.55已在两组开发样例核对，不是通用正确概率")
    ax.bar(["周末开门\n开发","火星燃料\n开发","通知冲突\n测试","无线网络\n测试","海王星\n测试"],values,color=["#4878b8","#b8c6d5","#ba8740","#ba8740","#b8c6d5"])
    ax.axhline(.55,color="#9b554f",linestyle="--",label="教学门槛 0.55")
    ax.set_ylim(0,1);ax.legend(fontsize=12)
    for i,value in enumerate(values):ax.text(i,value+.025,f"{value:.4f}",ha="center",fontsize=12)
    save_figure(fig,ROOT/"assets","retrieval-scores")


if __name__=="__main__":draw()
