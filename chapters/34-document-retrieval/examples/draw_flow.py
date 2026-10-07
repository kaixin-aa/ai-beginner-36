from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure
ROOT=Path(__file__).resolve().parents[1]
def draw():
    configure_style();fig,ax=plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.05,right=.95,top=.85,bottom=.16);ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
    fig.suptitle('原文件与索引版本共同决定来源是否有效',fontsize=23,y=.94)
    labels=['TXT / MD / PDF\n原文件与哈希','文字单元\n页码、行号','切分与编码\n保留字符位置','完整新版本\n检查后切换','问题与引用\n原文逐字核对']
    for i,label in enumerate(labels):
        x=.015+i*.2
        ax.add_patch(FancyBboxPatch((x,.57),.165,.27,boxstyle='round,pad=.008',facecolor='#eaf2ff'if i<3 else'#e0f1ec',edgecolor='#8296aa'))
        ax.text(x+.0825,.705,label,ha='center',va='center',fontsize=13,linespacing=1.7)
        if i<4:ax.annotate('',xy=(x+.195,.705),xytext=(x+.175,.705),arrowprops={'arrowstyle':'->','lw':1.6})
    ax.text(.5,.33,'新增资料先重建；删除时清理旧索引与相关请求记录',ha='center',fontsize=16)
    ax.text(.5,.16,'PDF位置对应抽取文本与原页，不承诺还原复杂页面排版',ha='center',fontsize=14,color='#536275')
    fig.text(.05,.055,'原创教学图   四份原创资料、五个512维片段，固定公开模型在本机运行',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','document-index-flow')
    fig,ax=plt.subplots(figsize=(10,6.25),dpi=160);fig.subplots_adjust(left=.08,right=.92,top=.84,bottom=.16)
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1));fig.suptitle('一条PDF引用如何定位',fontsize=23,y=.94)
    ax.text(.5,.84,'文件   equipment.pdf       页码   第2页',ha='center',fontsize=19)
    ax.text(.5,.66,'源页文字单元中查找连续原文',ha='center',fontsize=17)
    ax.add_patch(FancyBboxPatch((.05,.32),.9,.22,boxstyle='round,pad=.01',facecolor='#e0f1ec',edgecolor='#8296aa'))
    ax.text(.5,.43,'先关闭电源，再归还到服务台。',ha='center',va='center',fontsize=22)
    ax.annotate('',xy=(.5,.57),xytext=(.5,.62),arrowprops={'arrowstyle':'->','lw':1.8})
    ax.text(.5,.15,'字符起点从0计数，结束点不包含末端字符；行号从1开始',ha='center',fontsize=13,color='#536275')
    fig.text(.06,.055,'原创教学图   引用必须存在于本轮检索片段及原页文字中，文件哈希也需一致',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','pdf-citation-position')
if __name__=='__main__':draw()
