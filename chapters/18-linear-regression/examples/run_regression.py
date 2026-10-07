"""输出清洗表、三模型结果、参数、残差与原创回归图。"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from regression_core import prepare_data, run_experiment
from plot_style import configure_style, new_figure, save_figure

ROOT = Path(__file__).resolve().parents[1]
LABELS = {"baseline": "均值基线", "single": "单特征", "multi": "三特征"}


def main():
    clean, rejected, cleaning = prepare_data()
    models, train, test, summary = run_experiment(clean)
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    for name, frame in [("clean_records", clean), ("rejected_records", rejected), ("train_rows", train), ("test_predictions", test)]:
        frame.to_csv(results / f"{name}.csv", index=False, lineterminator="\n")
    rows = [{"model": name, "split": split, **values} for name, scores in summary["scores"].items() for split, values in scores.items() if split in ["train", "test"]]
    pd.DataFrame(rows).to_csv(results / "metrics.csv", index=False, lineterminator="\n")
    summary["cleaning"] = cleaning
    (results / "regression-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    configure_style()
    assets = ROOT / "assets"
    fig, ax = new_figure("单特征回归，在训练记录上拟合一条直线", "engine_size（原表量纲）", "price（原表价格数值）", "UCI Automobile 1985 历史数据；蓝点为训练记录，橙点为保留的测试记录。")
    ax.scatter(train.engine_size, train.price, s=24, alpha=0.65, label=f"训练 n={len(train)}")
    ax.scatter(test.engine_size, test.price, s=36, color="#e48832", label=f"测试 n={len(test)}")
    grid = np.linspace(train.engine_size.min(), train.engine_size.max(), 100)
    ax.plot(grid, models["single"].predict(pd.DataFrame({"engine_size": grid})), color="#415669", label="只用训练集拟合")
    ax.legend(fontsize=12)
    save_figure(fig, assets, "single-feature-fit")

    fig, ax = new_figure("相同测试集上的真实值与预测值", "真实 price（原表价格数值）", "预测 price（原表价格数值）", f"同一份测试集 n={len(test)}；虚线表示预测恰好等于真实值；均值基线形成水平点列。")
    for name in models:
        ax.scatter(test.price, test[f"{name}_prediction"], s=45, alpha=0.7, label=LABELS[name])
    upper = max(test.price.max(), test.multi_prediction.max(), test.single_prediction.max())*1.07
    ax.plot([0, upper], [0, upper], linestyle="--", color="#64788c", label="理想预测")
    ax.set(xlim=(0, upper), ylim=(min(0, test.multi_prediction.min(), test.single_prediction.min())-1000, upper))
    ax.legend(fontsize=12, loc="upper left")
    save_figure(fig, assets, "actual-vs-predicted")

    fig, ax = new_figure("三特征模型，残差在高价格记录上更大", "真实 price（原表价格数值）", "残差（真实值减预测值）", "同一测试集；零线以上表示低估，以下表示高估；标注为绝对误差最大的 3 条。")
    ax.scatter(test.price, test.multi_residual, s=60, color="#2678b8")
    ax.axhline(0, linestyle="--", color="#64788c")
    offsets = [(-8, 12, "right"), (-20, 32, "right"), (10, -25, "left")]
    for index, (_, row) in enumerate(test.sort_values("multi_absolute_error", ascending=False).head(3).iterrows()):
        dx, dy, alignment = offsets[index]
        ax.annotate(row.sample_id, (row.price, row.multi_residual), xytext=(dx, dy), textcoords="offset points", fontsize=12, ha=alignment, arrowprops={"arrowstyle": "-", "color": "#64788c", "lw": 0.7})
    fig.subplots_adjust(left=0.16)
    ax.margins(x=0.1, y=0.16)
    save_figure(fig, assets, "multi-feature-residuals")
    print("清洗", cleaning)
    print("训练/测试", len(train), len(test))
    print("参数", summary["parameters"])
    for row in rows:
        print(row["model"], row["split"], f"MAE={row['MAE']:.2f} RMSE={row['RMSE']:.2f} R2={row['R2']:.4f}")
    print("误差最大的三条", test.sort_values("multi_absolute_error", ascending=False).head(3)[["sample_id", "price", "multi_prediction", "multi_residual"]].to_dict("records"))


if __name__ == "__main__":
    main()
