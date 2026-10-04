"""原创请求往返图及错误处理图，保存可编辑 SVG。"""
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
from plot_style import configure_style, plt, save_figure

ROOT = Path(__file__).resolve().parents[1]


def draw():
    configure_style()
    fig, ax = plt.subplots(figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.16)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    fig.suptitle("一次问答怎样完成 HTTP 往返", fontsize=23, y=0.95)
    names = ["输入问题", "读取配置", "发送请求", "服务生成", "解析响应"]
    notes = ["中文字符串", "地址和模型\n本机环境密钥", "POST\nJSON 消息", "模型运行\n本机没有训练", "回答及用量\n检查结束原因"]
    colors = ["#eaf3ff", "#eaf3ff", "#dff2ed", "#dff2ed", "#fff0d5"]
    for i, (name, note, color) in enumerate(zip(names, notes, colors)):
        x = 0.01 + i * 0.2
        ax.add_patch(FancyBboxPatch((x, 0.48), 0.17, 0.33, boxstyle="round,pad=0.006", facecolor=color, edgecolor="#8195ac"))
        ax.text(x+0.085, 0.72, name, ha="center", va="center", fontsize=16)
        ax.text(x+0.085, 0.595, note, ha="center", va="center", fontsize=13, linespacing=1.6)
        if i < 4:
            ax.annotate("", xy=(x+0.195, 0.65), xytext=(x+0.176, 0.65), arrowprops={"arrowstyle": "->", "lw": 1.7, "color": "#42627e"})
    ax.text(0.5, 0.33, "客户端等待响应，再把可公开的结果保存成 JSON", ha="center", fontsize=17)
    ax.text(0.5, 0.16, "Authorization 携带认证信息，不进入记录文件", ha="center", fontsize=15, color="#536275")
    fig.text(0.05, 0.07, "原创教学图   本地固定响应只验证传输；真实模型结果另行记录", fontsize=13, color="#536275")
    save_figure(fig, ROOT / "assets", "api-roundtrip")

    fig, ax = plt.subplots(figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.83, bottom=0.17)
    ax.axis("off")
    fig.suptitle("遇到错误后，先判断该改什么", fontsize=23, y=0.94)
    rows = [
        ("配置缺失", "请求还没发送", "在本机设置环境变量"),
        ("HTTP 401 / 402", "认证失败或余额不足", "检查密钥与平台余额"),
        ("HTTP 400 / 422", "请求格式或参数无效", "修正配置与请求内容"),
        ("HTTP 429 / 503", "限流或服务繁忙", "稍后手动重试"),
        ("请求超时", "是否已生成，结果未知", "检查后决定是否重试"),
    ]
    for i, (event, meaning, action) in enumerate(rows):
        y = 0.86 - i * 0.17
        ax.add_patch(FancyBboxPatch((0.01, y-0.07), 0.97, 0.14, boxstyle="round,pad=0.005", facecolor="#f1f5f9" if i % 2 == 0 else "#e8f2ef", edgecolor="#d0dce7"))
        ax.text(0.04, y, event, va="center", fontsize=14)
        ax.text(0.30, y, meaning, va="center", fontsize=14)
        ax.text(0.67, y, action, va="center", fontsize=14)
    fig.text(0.06, 0.065, "原创教学图   本章默认不自动重试，避免一次操作发出多次付费请求", fontsize=13, color="#536275")
    save_figure(fig, ROOT / "assets", "api-error-actions")


if __name__ == "__main__":
    draw()
