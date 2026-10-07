from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure
ROOT=Path(__file__).resolve().parents[1]

def canvas(title):
    configure_style();fig,ax=plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.05,right=.95,top=.85,bottom=.15)
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1));fig.suptitle(title,fontsize=23,y=.94)
    return fig,ax

def box(ax,x,y,w,h,text,color='#eaf2ff',size=14):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.01',facecolor=color,edgecolor='#8296aa'))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,linespacing=1.6)

def arrow(ax,start,end):ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1.7})

def draw():
    fig,ax=canvas('个人知识库助手页面草图')
    box(ax,.02,.12,.33,.74,'资料区\n\n选择文件  ·  导入\n资料名称与处理状态\n建立 / 更新索引\n确认后删除资料','#eaf2ff',15)
    box(ax,.4,.64,.57,.22,'问题输入框   ·   提问\n没有有效索引时说明原因','#e0f1ec',16)
    box(ax,.4,.33,.57,.24,'回答区\n有依据 / 资料不足 / 冲突\n回答文字、请求用量与耗时',size=15)
    box(ax,.4,.05,.57,.20,'展开引用\n文件名、PDF页码或行号、原文','#f5e8da',15)
    fig.text(.05,.055,'原创设计草图   当前未实现网页；第一版只供一位使用者在本机运行',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','page-sketch')
    fig,ax=canvas('五个模块分别负责一段处理')
    labels=['文件导入\n格式与大小','文档保存\n原文和哈希','知识索引\n片段与向量','资料问答\n检索与引用','本机网页\n操作和反馈']
    for i,label in enumerate(labels):
        box(ax,.015+i*.2,.61,.165,.26,label,'#e0f1ec'if i==4 else'#eaf2ff',13)
        if i<4:arrow(ax,(.19+i*.2,.74),(.207+i*.2,.74))
    box(ax,.24,.12,.52,.25,'公共格式与运行配置\n固定来源位置、索引版本及密钥变量','#f5e8da',15)
    for x in(.1,.5,.9):arrow(ax,(x,.60),(.5,.38))
    fig.text(.05,.055,'原创模块图   网页负责呈现，后端负责校验；文件保存只由用户导入动作触发',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','module-map')
    fig,ax=canvas('导入与提问采用两条明确的请求流程')
    top=['人选择文件','校验与抽取','登记来源','重建索引'];bottom=['人输入问题','检查索引','检索与生成','引用核对展示']
    for y,labels,color in ((.61,top,'#eaf2ff'),(.18,bottom,'#e0f1ec')):
        for i,label in enumerate(labels):
            box(ax,.025+i*.25,y,.2,.2,label,color,14)
            if i<3:arrow(ax,(.235+i*.25,y+.1),(.264+i*.25,y+.1))
    arrow(ax,(.875,.60),(.375,.39))
    ax.text(.15,.46,'导入后由人点击更新',fontsize=13,color='#536275')
    fig.text(.05,.055,'原创请求图   检索为空直接返回；有片段才请求模型，生成失败显示失败原因',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','request-flow')

if __name__=='__main__':draw()
