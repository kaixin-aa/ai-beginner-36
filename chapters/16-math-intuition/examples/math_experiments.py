"""导出四张数学直觉图、梯度下降轨迹和可核对结果。"""
import csv
import json
from pathlib import Path
import numpy as np
from math_core import descent, finite_difference, gradient
from plot_style import configure_style, new_figure, save_figure, plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    font = configure_style()
    assets = ROOT / "assets"
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    groups = {"A 组": np.array([18, 20, 22]), "B 组": np.array([10, 20, 30])}
    statistics = {name: {"values": values.tolist(), "mean": float(values.mean()), "variance_ddof0": float(values.var()), "std_ddof0": float(values.std())} for name, values in groups.items()}
    fig, ax = new_figure("均值相同，分散程度不同", "学习时长（分钟）", "教学分组", "原创虚构数据，每组 3 条；方差使用除以 N 的定义，单位为分钟平方。")
    for y, (name, values) in enumerate(groups.items()):
        ax.scatter(values, [y] * 3, s=180, color=["#2678b8", "#e48832"][y], zorder=3)
        ax.plot([values.min(), values.max()], [y, y], color="#a3b4c8", zorder=1)
        for value in values:
            ax.annotate(str(value), (value, y), xytext=(0, 18), textcoords="offset points", ha="center")
    ax.axvline(20, color="#65778b", linestyle="--", label="两组均值均为 20")
    ax.set_yticks([0, 1], ["A 组  方差 2.67", "B 组  方差 66.67"])
    ax.set(xlim=(7, 33), ylim=(-0.5, 1.6))
    fig.subplots_adjust(left=0.25)
    ax.legend(loc="upper left", fontsize=13)
    save_figure(fig, assets, "mean-variance")

    fig, ax = new_figure("公平骰子，偶数事件的概率为 1/2", "一次投掷的点数", "单个点数的理论概率", "假设六个点数等可能；橙色为偶数；理论模型，未使用真实投掷数据。")
    faces = np.arange(1, 7)
    ax.bar(faces, np.full(6, 1 / 6), color=["#e48832" if face % 2 == 0 else "#2678b8" for face in faces], width=0.65)
    for face in faces:
        ax.text(face, 1 / 6 + 0.007, "1/6", ha="center", fontsize=16)
    ax.set_xticks(faces)
    ax.set(ylim=(0, 0.23))
    save_figure(fig, assets, "probability")

    x = np.linspace(-1, 10, 300)
    y = (x - 3) ** 2 + 1
    fig, ax = new_figure("函数是一条输入到输出的规则", "参数 w", "损失 L(w)", "原创教学函数 L(w)=(w-3)²+1；w=5 处切线斜率为 4。")
    ax.plot(x, y, color="#2678b8", label="损失曲线")
    tangent_x = np.linspace(3.8, 6.2, 50)
    ax.plot(tangent_x, 5 + 4 * (tangent_x - 5), color="#e48832", label="w=5 处切线")
    ax.scatter([3, 5, 9], [1, 5, 37], color="#e48832", zorder=3)
    for point, label in [((3, 1), "最低点 (3, 1)"), ((5, 5), "(5, 5)"), ((9, 37), "(9, 37)")]:
        ax.annotate(label, point, xytext=(8, 12), textcoords="offset points", fontsize=13)
    ax.set(ylim=(-2, 56), xlim=(-1, 10))
    ax.legend(loc="upper left", fontsize=13)
    save_figure(fig, assets, "function-derivative")

    history = descent()
    rates = {str(rate): descent(9, rate, 12) for rate in [0.01, 0.2, 1.0, 1.1]}
    fig, axes = plt.subplots(1, 2, figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.78, bottom=0.23, wspace=0.32)
    fig.suptitle("梯度下降每次重新计算当前位置的斜率", fontsize=22, y=0.94)
    left, right = axes
    left.plot(x, y, color="#2678b8")
    shown = history[:4]
    left.plot([row["w"] for row in shown], [row["loss"] for row in shown], "o-", color="#e48832")
    for row in shown:
        left.annotate(str(row["step"]), (row["w"], row["loss"]), xytext=(6, 8), textcoords="offset points", fontsize=13)
    left.set(xlabel="参数 w", ylabel="损失", title="前 3 次更新", xlim=(1, 10), ylim=(0, 52))
    for rate, records in rates.items():
        right.plot([row["step"] for row in records], [row["loss"] for row in records], label=f"学习率 {rate}")
    right.set(xlabel="更新次数", ylabel="损失（对数刻度）", title="步长决定变化", yscale="log")
    right.legend(fontsize=11)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(color="#dfe5ec", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.title.set_fontsize(17)
    fig.text(0.06, 0.06, "原创教学函数；编号 0 是初始位置；学习率 1.0 振荡，1.1 发散。", fontsize=12, color="#536275")
    save_figure(fig, assets, "gradient-descent")
    summary = {"teaching_only": True, "font": font, "statistics": statistics, "fair_die_even_probability": 0.5, "gradient_at_5": gradient(5), "finite_difference_at_5": finite_difference(5), "history": history, "learning_rate_experiments": rates}
    (results / "math-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (results / "descent-steps.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "w", "loss", "gradient"])
        writer.writeheader()
        writer.writerows(history)
    print("两组均值", [item["mean"] for item in statistics.values()])
    print("两组方差", [item["variance_ddof0"] for item in statistics.values()])
    for row in history[:4] + history[-1:]:
        print(f"第 {row['step']} 步 w={row['w']:.6f} loss={row['loss']:.6f} gradient={row['gradient']:.6f}")
    print("四张图已导出 PNG 与 SVG")


if __name__ == "__main__":
    main()
