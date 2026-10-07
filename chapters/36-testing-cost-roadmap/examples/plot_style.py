"""中文图表的字体与导出设置，仅使用 Matplotlib。"""
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt


def configure_style():
    windows_font = Path("C:/Windows/Fonts/msyh.ttc")
    if windows_font.exists():
        font_manager.fontManager.addfont(str(windows_font))
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "WenQuanYi Zen Hei"]
    for name in candidates:
        try:
            font_manager.findfont(name, fallback_to_default=False)
            chosen = name
            break
        except ValueError:
            continue
    else:
        raise RuntimeError("未找到中文字体，请安装 Noto Sans CJK SC 或修改候选字体名称")
    plt.rcParams.update({"font.family": chosen, "axes.unicode_minus": False, "font.size": 16, "axes.titlesize": 22, "axes.labelsize": 17, "svg.fonttype": "none"})
    return chosen


def new_figure(title, xlabel, ylabel, note):
    fig, ax = plt.subplots(figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.12, right=0.94, top=0.83, bottom=0.22)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#dfe5ec", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.text(0.08, 0.055, note, fontsize=12, color="#536275")
    return fig, ax


def save_figure(fig, folder, name):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    fig.savefig(folder / f"{name}.png", dpi=160)
    fig.savefig(folder / f"{name}.svg")
    plt.close(fig)
