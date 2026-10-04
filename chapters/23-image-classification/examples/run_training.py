import csv
import json
from pathlib import Path
import numpy as np
import torch
from image_core import train_model, save_model, load_model, pixels_to_tensor, load_single_image, predict_image
from plot_style import configure_style, plt, new_figure, save_figure

ROOT = Path(__file__).resolve().parents[1]


def main():
    model, images, labels, train, test, prediction, history, summary = train_model()
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    path = results / "digits-state.pt"
    save_model(model, path)
    restored = load_model(path)
    with torch.no_grad():
        a = model(pixels_to_tensor(images[test]))
        b = restored(pixels_to_tensor(images[test]))
    assert torch.equal(a, b)
    summary["reload_logits_identical"] = True
    summary["single_png_prediction"] = predict_image(restored, load_single_image(ROOT / "data/sample-digit.png"))
    wrong = test[prediction != labels[test]]
    summary["wrong_source_indices"] = wrong.tolist()
    matrix = np.zeros((10, 10), dtype=int)
    np.add.at(matrix, (labels[test], prediction), 1)
    summary["confusion_matrix"] = matrix.tolist()
    (results / "training-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (results / "training-history.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=history[0].keys())
        writer.writeheader()
        writer.writerows(history)
    with (results / "test-predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_index", "true_label", "prediction", "correct"])
        writer.writerows((int(i), int(labels[i]), int(p), bool(labels[i] == p)) for i, p in zip(test, prediction))
    with (results / "split-manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_index", "split", "label"])
        writer.writerows((int(i), split, int(labels[i])) for split, indices in [("train", train), ("test", test)] for i in indices)
    configure_style()
    assets = ROOT / "assets"
    fig, axes = plt.subplots(1, 2, figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.09, right=0.96, top=0.81, bottom=0.22, wspace=0.32)
    fig.suptitle("小型全连接网络的训练记录", fontsize=22, y=0.94)
    axes[0].plot([r["epoch"] for r in history], [r["train_loss"] for r in history])
    axes[0].set(xlabel="训练轮次", ylabel="训练交叉熵损失", title="训练损失")
    axes[1].plot([r["epoch"] for r in history], [r["train_accuracy"] for r in history])
    axes[1].set(xlabel="训练轮次", ylabel="训练准确率", title="训练准确率", ylim=(0, 1.05))
    for ax in axes:
        ax.grid(color="#dfe5ec")
        ax.title.set_fontsize(17)
    fig.text(0.06, 0.055, "公开 digits 数据；第 0 轮为初始状态；测试集只在预设 30 轮结束后评估。", fontsize=12)
    save_figure(fig, assets, "training-curves")

    fig, ax = new_figure("最终测试集的混淆矩阵", "预测数字", "真实数字", f"固定测试集 n={len(test)}；对角线为正确分类；样本未参与训练。")
    ax.imshow(matrix, cmap="Blues", interpolation="nearest")
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.grid(False)
    for i in range(10):
        for j in range(10):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=11, color="white" if matrix[i, j]>matrix.max()/2 else "#24394d")
    save_figure(fig, assets, "confusion-matrix")

    selected = wrong[:8] if len(wrong) else test[:8]
    fig, axes = plt.subplots(2, 4, figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.79, bottom=0.16, hspace=0.5, wspace=0.35)
    fig.suptitle("保留分错图片，回到像素检查", fontsize=22, y=0.94)
    predicted_by_id = dict(zip(test.tolist(), prediction.tolist()))
    for ax, index in zip(axes.ravel(), selected):
        ax.imshow(images[index], cmap="gray", vmin=0, vmax=16, interpolation="nearest")
        ax.set_title(f"编号 {index}\n真 {labels[index]} / 预测 {predicted_by_id[index]}", fontsize=13)
        ax.axis("off")
    for ax in axes.ravel()[len(selected):]:
        ax.axis("off")
    fig.text(0.06, 0.045, "按固定测试记录顺序取前 8 条错误；图像来自公开数据，图版布局为原创。", fontsize=12)
    save_figure(fig, assets, "wrong-examples")
    print("训练/测试", len(train), len(test), "每轮批次", summary["batches_per_epoch"], "更新次数", summary["optimizer_updates"])
    print("最终训练", summary["final_train"], "测试", summary["test"])
    print("训练用时秒", round(summary["training_seconds"], 3), "参数数", summary["parameters"])
    print("重载一致", summary["reload_logits_identical"], "单图预测", summary["single_png_prediction"]["label"])


if __name__ == "__main__":
    main()
