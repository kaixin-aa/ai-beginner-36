"""生成三个问题的统计与原创图表。"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from analysis import BINS, load_records, summarize
from plot_style import configure_style, new_figure, save_figure


def make_charts(frame, summary, assets):
    font = configure_style()
    known = frame.loc[frame["minutes"].notna()].copy()
    values = known["minutes"].to_numpy(dtype=float)
    fig, ax = new_figure("已知学习时长的分布", "学习时长（分钟）", "记录数量（条）", "虚构教学数据；3 条时长已知，2 条未知被排除。\n区间左闭右开，最后一个区间包含右端；纵轴使用计数。")
    ax.hist(values, bins=BINS, color="#2879bd", edgecolor="white")
    ax.set_xticks(BINS)
    ax.set_yticks([0, 1, 2])
    ax.set_ylim(0, 1.5)
    save_figure(fig, assets, "minutes-histogram")

    groups = pd.DataFrame(summary["groups"])
    fig, ax = new_figure("不同标签的记录数量与完成数量", "学习标签", "记录数量（条）", "使用全部 5 条虚构教学记录；每个标签各有 1 条时长未知。\n完成比例按完成条数 / 全部条数计算，不按时长筛选。")
    x = np.arange(len(groups))
    ax.bar(x - 0.18, groups["records"], width=0.36, label="全部记录", color="#b7d6ed")
    bars = ax.bar(x + 0.18, groups["completed"], width=0.36, label="已完成", color="#2879bd")
    ax.set_xticks(x, groups["tag"])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_ylim(0, 4.1)
    for bar, rate in zip(bars, groups["completion_rate"]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.12, f"完成比例 {rate:.1%}", ha="center", fontsize=12)
    ax.legend(loc="upper left", frameon=False)
    save_figure(fig, assets, "tag-completion-bars")

    fig, ax = new_figure("已知时长与完成状态", "学习时长（分钟）", "完成状态", "仅使用时长已知的 3 条虚构记录；未完成编码 0，完成编码 1。\n点的关系描述当前样本，不能推断学习时长的因果效果。")
    fig.subplots_adjust(left=0.25)
    ax.scatter(values, known["done"].astype(int), s=110, color="#2879bd")
    for row in known.itertuples():
        ax.annotate(str(row.record_id), (float(row.minutes), int(row.done)), xytext=(8, 10), textcoords="offset points", fontsize=13)
    ax.set_yticks([0, 1], ["未完成（0）", "已完成（1）"])
    ax.set_ylim(-0.25, 1.35)
    ax.set_xlim(10, 45)
    save_figure(fig, assets, "minutes-completion-scatter")
    return font


def main():
    chapter = Path(__file__).resolve().parents[1]
    source = chapter / "data/learning_records.csv"
    frame = load_records(source)
    summary = summarize(frame)
    summary["data_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    summary["font"] = make_charts(frame, summary, chapter / "assets")
    results = chapter / "results"
    results.mkdir(exist_ok=True)
    (results / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    pd.DataFrame(summary["groups"]).to_csv(results / "group_summary.csv", index=False, encoding="utf-8")
    print("全部记录", summary["input_rows"], "时长已知", summary["known_minutes_rows"], "时长未知", summary["missing_minutes_rows"])
    print("已知时长均值", summary["known_mean"], "中位数", summary["known_median"])
    print("直方图计数", summary["histogram_counts"])
    print("当前样本相关系数", summary["pearson_r"])
    print("已保存三张 PNG、三份 SVG 和统计结果")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
