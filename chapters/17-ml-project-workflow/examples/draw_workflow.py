"""原创项目流程图，显示测试行不进入 fit 的分支。"""
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style, plt, save_figure


def main():
    configure_style()
    fig, ax = plt.subplots(figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.12)
    ax.set(xlim=(0, 10), ylim=(0, 6))
    ax.axis("off")
    fig.suptitle("一个机器学习项目中，数据怎样流动", fontsize=23, y=0.96)

    def box(x, y, text, color="#eaf3fb", width=3.6, height=0.9):
        ax.add_patch(FancyBboxPatch((x-width/2, y-height/2), width, height, boxstyle="round,pad=0.08", facecolor=color, edgecolor="#8eabc5", linewidth=1.4))
        ax.text(x, y, text, ha="center", va="center", fontsize=15, linespacing=1.5)

    def arrow(start, end, text=None):
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": "#506b85", "lw": 2})
        if text:
            ax.text((start[0]+end[0])/2, (start[1]+end[1])/2, text, fontsize=12, ha="center", bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})

    box(2.4, 5.2, "明确任务\n用 4 个测量值判断花卉类别")
    box(7.6, 5.2, "公开数据 150 条\nX、y、编号保持配对")
    arrow((4.3, 5.2), (5.7, 5.2))
    box(7.6, 3.7, "固定划分并保留编号\n分层随机抽取，种子 42")
    arrow((7.6, 4.7), (7.6, 4.25))
    box(2.4, 2.3, "训练集 120 条\nfit 标准化与分类器", "#e7f5ed")
    box(7.6, 2.3, "测试集 30 条\npredict 后对照真实标签", "#fff0e1")
    arrow((5.7, 3.7), (2.4, 2.85), "训练分支")
    arrow((7.6, 3.2), (7.6, 2.85))
    arrow((4.3, 2.3), (5.7, 2.3), "已训练模型")
    box(2.4, 0.65, "保存完整 Pipeline\n同时记录字段顺序与版本")
    box(7.6, 0.65, "重载后接收单条输入\n按相同顺序与单位预测")
    arrow((2.4, 1.8), (2.4, 1.2))
    arrow((4.3, 0.65), (5.7, 0.65))
    fig.text(0.07, 0.035, "原创流程图；测试行不进入任何 fit；训练结果与测试结果分别记录。", fontsize=12, color="#536275")
    save_figure(fig, Path(__file__).resolve().parents[1] / "assets", "project-workflow")


if __name__ == "__main__":
    main()
