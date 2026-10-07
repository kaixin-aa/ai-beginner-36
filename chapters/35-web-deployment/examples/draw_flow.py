from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure
ROOT=Path(__file__).resolve().parents[1]
def draw():
    configure_style();fig,ax=plt.subplots(figsize=(10,6.25),dpi=160);fig.subplots_adjust(left=.05,right=.95,top=.85,bottom=.16)
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1));fig.suptitle('密钥留在后端，网页只接收结果',fontsize=23,y=.94)
    labels=['本机浏览器\n导入、提问','本机Python服务\n校验与检索','固定模型接口\n只生成一次','回答与引用\n原文和用量']
    for i,label in enumerate(labels):
        x=.02+i*.25;ax.add_patch(FancyBboxPatch((x,.56),.205,.28,boxstyle='round,pad=.01',facecolor='#eaf2ff'if i in(0,3)else'#e0f1ec',edgecolor='#8296aa'))
        ax.text(x+.1025,.70,label,ha='center',va='center',fontsize=14,linespacing=1.7)
        if i<3:ax.annotate('',xy=(x+.24,.70),xytext=(x+.215,.70),arrowprops={'arrowstyle':'->','lw':1.6})
    ax.text(.5,.33,'空问题与错误文件先检查；执行时暂时禁用按钮',ha='center',fontsize=16)
    ax.text(.5,.14,'默认回环监听；实际线上部署未执行，不能替代为本机截图',ha='center',fontsize=14,color='#536275')
    fig.text(.05,.055,'原创教学图   API密钥不进入HTML或浏览器请求，页面可见原文与实际用量',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','web-service-flow')
if __name__=='__main__':draw()
