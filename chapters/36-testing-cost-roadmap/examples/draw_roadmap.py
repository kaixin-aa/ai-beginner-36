from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure
ROOT=Path(__file__).resolve().parents[1]
def draw():
    configure_style();fig,ax=plt.subplots(figsize=(10,6.25),dpi=160);fig.subplots_adjust(left=.05,right=.95,top=.85,bottom=.16)
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1));fig.suptitle('从同一个作品选择下一项可执行任务',fontsize=23,y=.94)
    rows=[(.66,'AI应用开发','拆出Web API，再实现用户与资料隔离','#eaf2ff'),(.36,'机器学习','复用Iris，比较五折验证与保留测试','#e0f1ec'),(.06,'模型训练','复用小型CNN，记录三个随机种子的结果','#f5e8da')]
    for y,title,task,color in rows:
        ax.add_patch(FancyBboxPatch((.03,y),.94,.22,boxstyle='round,pad=.01',facecolor=color,edgecolor='#8296aa'))
        ax.text(.07,y+.13,title,fontsize=17,va='center');ax.text(.34,y+.13,task,fontsize=14,va='center')
    fig.text(.05,.055,'原创学习路线图   每次完成一项变化并保存验证证据，不要求一次学习全部方向',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','learning-roadmap')
if __name__=='__main__':draw()
