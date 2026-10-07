from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style, plt, save_figure
ROOT = Path(__file__).resolve().parents[1]


def box(ax, x, y, width, height, text, color, fontsize=15):
    ax.add_patch(FancyBboxPatch((x,y),width,height,boxstyle="round,pad=0.008",facecolor=color,edgecolor="#8296aa"))
    ax.text(x+width/2,y+height/2,text,ha="center",va="center",fontsize=fontsize,linespacing=1.4)


def draw():
    configure_style()
    fig, ax = plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=0.04,right=0.96,top=0.86,bottom=0.19)
    ax.axis("off")
    ax.set(xlim=(0,1),ylim=(0,1))
    fig.suptitle("对话历史按完整消息对裁剪",fontsize=23,y=0.94)
    ax.text(0.23,0.96,"已经保存的历史",ha="center",fontsize=17)
    ax.text(0.75,0.96,"本轮实际发送",ha="center",fontsize=17)
    labels=["用户 1", "助手 1", "用户 2", "助手 2", "用户 3", "助手 3"]
    for i,label in enumerate(labels):
        y=0.79-i*0.13
        color="#f0f0f0" if i<4 else "#e0f1ec"
        box(ax,0.06,y,0.34,0.10,label+("   移除" if i<4 else "   保留"),color,14)
    for i,label in enumerate(["系统要求及当前分钟预算","用户 3","助手 3","最新用户需求"]):
        box(ax,0.54,0.76-i*0.17,0.40,0.13,label,"#eaf2ff" if i in (0,3) else "#e0f1ec",14)
    ax.annotate("",xy=(0.52,0.39),xytext=(0.42,0.18),arrowprops={"arrowstyle":"->","lw":1.8,"color":"#42627e"})
    fig.text(0.05,0.08,"原创教学图   图示最多保留一对；程序默认三对、2000字符预算，字符数不等于Token数",fontsize=12,color="#536275")
    save_figure(fig,ROOT/"assets","history-trimming")

    fig, ax=plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=0.04,right=0.96,top=0.85,bottom=0.17)
    ax.axis("off")
    ax.set(xlim=(0,1),ylim=(0,1))
    fig.suptitle("有效 JSON 还要通过字段和分钟校验",fontsize=23,y=0.94)
    labels=["收到文本", "JSON 解析", "字段与类型", "任务分钟求和", "保存有效计划"]
    notes=["检查结束原因", "文本变成对象", "缺字段即失败", "等于当前预算", "更新对话历史"]
    for i,(label,note) in enumerate(zip(labels,notes)):
        x=0.015+i*0.20
        box(ax,x,0.55,0.165,0.26,label+"\n"+note,"#eaf2ff" if i<3 else "#e0f1ec",13)
        if i<4:
            ax.annotate("",xy=(x+0.193,0.68),xytext=(x+0.173,0.68),arrowprops={"arrowstyle":"->","lw":1.7})
    box(ax,0.20,0.12,0.60,0.22,"失败后最多请求一次格式修复\n两次仍失败，原会话保持不变","#fff0d5",16)
    ax.annotate("",xy=(0.5,0.35),xytext=(0.5,0.52),arrowprops={"arrowstyle":"->","lw":1.8,"color":"#b67c36"})
    fig.text(0.06,0.055,"原创教学图   JSON模式约束格式；本地校验检查字段、类型与业务要求",fontsize=13,color="#536275")
    save_figure(fig,ROOT/"assets","json-validation")


if __name__ == "__main__":
    draw()
