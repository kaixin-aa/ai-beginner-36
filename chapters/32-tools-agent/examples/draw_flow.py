from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style,plt,save_figure
ROOT=Path(__file__).resolve().parents[1]

def canvas(title):
    configure_style()
    fig,ax=plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.05,right=.95,top=.85,bottom=.15)
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
    fig.suptitle(title,fontsize=23,y=.94)
    return fig,ax

def box(ax,x,y,w,h,text,color='#eaf2ff'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.01',facecolor=color,edgecolor='#8296aa'))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=14,linespacing=1.8)

def arrow(ax,start,end):ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1.7})

def draw():
    fig,ax=canvas('模型提议，程序校验，再把工具结果送回模型')
    box(ax,.02,.62,.25,.25,'问题与已有消息\n送入模型')
    box(ax,.37,.62,.25,.25,'工具名称与参数\n程序整批校验')
    box(ax,.72,.62,.25,.25,'只读搜索 / 计算器\n程序执行工具','#e0f1ec')
    box(ax,.37,.14,.25,.25,'tool 消息带调用编号\n下一轮读取结果','#e0f1ec')
    box(ax,.02,.14,.25,.25,'最终回答或停止状态\n保留完整记录')
    arrow(ax,(.28,.75),(.36,.75));arrow(ax,(.63,.75),(.71,.75))
    arrow(ax,(.84,.61),(.63,.27));arrow(ax,(.36,.27),(.145,.61))
    arrow(ax,(.145,.61),(.145,.40))
    ax.text(.81,.29,'未知工具、重复、超限\n直接停止',ha='center',fontsize=14,color='#9b554f')
    fig.text(.05,.055,'原创教学图   同一任务保留中间结果，计算器只解析允许的算术表达式',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','tool-cycle')
    fig,ax=canvas('执行权限由程序限定')
    box(ax,.03,.43,.42,.4,'允许的两个工具\n计算数字与读取固定教学资料\n不接受任意路径或网址','#e0f1ec')
    box(ax,.55,.43,.42,.4,'停止与预算\n最多6轮模型、4次工具\n步骤边界60秒，消息6000字符','#f5e8da')
    ax.text(.5,.24,'模型不能任意写文件、访问网站或执行系统命令',ha='center',fontsize=17)
    ax.text(.5,.08,'HTTP单次超时30秒；步骤时间限制不会强行打断正在运行的请求',ha='center',fontsize=13,color='#536275')
    fig.text(.05,.055,'原创教学图   这些数字是本章实现的教学限制，不是所有 Agent 的统一标准',fontsize=12,color='#536275')
    save_figure(fig,ROOT/'assets','tool-limits')

if __name__=='__main__':draw()
