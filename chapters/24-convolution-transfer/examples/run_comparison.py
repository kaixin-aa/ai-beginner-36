"""固定预算比较，从头训练、冻结特征、分两段微调；测试只在末次评估。"""
import csv
import json
import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt
from conv_core import ROOT, TEACHING_IMAGE, TEACHING_KERNEL, manual_correlation, pretrain, target_model, fit, evaluate, stack_dataset, save_target, load_target
from plot_style import configure_style, new_figure, save_figure

LABELS = {"scratch": "从头训练", "frozen": "冻结迁移", "fine_tune": "分段微调"}


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def draw_convolution(assets):
    result = manual_correlation(TEACHING_IMAGE, TEACHING_KERNEL)
    actual = torch.nn.functional.conv2d(torch.tensor(TEACHING_IMAGE)[None, None], torch.tensor(TEACHING_KERNEL)[None, None])[0, 0].numpy()
    np.testing.assert_array_equal(result, actual)
    steps = []
    for r in range(3):
        for c in range(3):
            steps.append({"row": r, "column": c, "top_left": float(TEACHING_IMAGE[r,c]), "bottom_right": float(TEACHING_IMAGE[r+1,c+1]), "output": float(result[r,c])})
    write_csv(ROOT / "results/convolution-steps.csv", steps)
    fig, axes = plt.subplots(1, 3, figsize=(10, 6.25), dpi=160)
    fig.subplots_adjust(left=.04, right=.96, top=.8, bottom=.27, wspace=.45)
    for ax, values, title in zip(axes, [TEACHING_IMAGE, TEACHING_KERNEL, result], ["① 输入 4×4", "② 共享核 2×2", "③ 输出 3×3"]):
        ax.imshow(values, cmap="Blues", vmin=-3, vmax=3)
        for (r,c), number in np.ndenumerate(values):
            ax.text(c, r, f"{number:g}", ha="center", va="center", color="black", fontsize=19)
        ax.set(title=title, xticks=[], yticks=[])
    fig.suptitle("同一组四个权重，逐格扫描图片", fontsize=23)
    fig.text(.08, .14, "首格 1×1 + 0×0 + 0×0 + 3×(−1) = −2\n右移一格 0×1 + 2×0 + 3×0 + 0×(−1) = 0", fontsize=15)
    fig.text(.08, .045, "原创教学数值；步长1，无填充，无偏置；按 PyTorch 互相关规则计算", fontsize=12)
    save_figure(fig, assets, "convolution-steps")


def draw_transfer(assets):
    fig, ax = plt.subplots(figsize=(10, 6.25), dpi=160)
    ax.set(xlim=(0,10), ylim=(0,6.25))
    ax.axis("off")
    for y, color, text in [(4.7,"#e4eefb","源任务 1000 张图\n卷积特征 → 十类数字头\n30轮预训练，保存特征"), (2.9,"#e5f4ed","新任务 120 张图\n复制特征 → 全新奇偶头\n冻结迁移或继续微调"), (1.1,"#fff0d9","目标测试 200 张图\n仅在固定训练结束后评估\n三个角色的原编号互不重叠")]:
        ax.text(5,y,text,ha="center",va="center",fontsize=18,bbox={"boxstyle":"round,pad=.6","fc":color,"ec":"#64748b"})
    for y in [4.02, 2.22]:
        ax.annotate("", xy=(5,y-.43), xytext=(5,y), arrowprops={"arrowstyle":"->","lw":2,"color":"#475569"})
    fig.suptitle("迁移的是特征参数，目标类别重新定义", fontsize=23)
    fig.text(.08,.045,"原创流程图；权重由本章自行预训练，源任务为十类数字",fontsize=12)
    save_figure(fig, assets, "transfer-flow")


def main():
    results, assets = ROOT / "results", ROOT / "assets"
    results.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    configure_style()
    pretrained, source_history, source_summary = pretrain()
    torch.save({"features": pretrained.features.state_dict(), "head": pretrained.head.state_dict(), "classes": list(range(10)), "torch": str(torch.__version__), "source_rows":1000}, results / "pretrained-digits.pt")
    # 实际从文件读取预训练特征再迁移，不依赖训练进程内的引用。
    source_payload = torch.load(results / "pretrained-digits.pt", map_location="cpu", weights_only=True)
    pretrained.features.load_state_dict(source_payload["features"])
    train_x, train_y, _ = stack_dataset("target_train")
    records, histories, models, predictions = [], {}, {}, {}
    initial_heads = []
    for mode in LABELS:
        model = target_model(mode, pretrained)
        initial_heads.append({k:v.clone() for k,v in model.head.state_dict().items()})
        before = {k:v.clone() for k,v in model.features.state_dict().items()}
        head_before = {k:v.clone() for k,v in model.head.state_dict().items()}
        history, timing = fit(model, train_x, train_y, 20, 42, mode)
        train_metric, _ = evaluate(model, train_x, train_y)
        record = {"mode": mode, **timing, "train": train_metric, "features_unchanged":all(torch.equal(v, model.features.state_dict()[k]) for k,v in before.items()), "head_changed":any(not torch.equal(v, model.head.state_dict()[k]) for k,v in head_before.items()), "trainable_first_10":66 if mode != "scratch" else 4274, "trainable_last_10":66 if mode == "frozen" else 4274}
        save_target(model, results / f"{mode}-state.pt", mode)
        models[mode] = model
        histories[mode] = history
        records.append(record)
    # 目标模型全部完成固定训练后才读取目标测试像素与标签。
    test_x, test_y, test_rows = stack_dataset("target_test")
    for record in records:
        mode = record["mode"]
        test_metric, predicted = evaluate(models[mode], test_x, test_y)
        loaded = load_target(results / f"{mode}-state.pt")
        with torch.no_grad():
            identical = torch.equal(models[mode](test_x), loaded(test_x))
        record.update({"test":test_metric, "reload_logits_identical":identical})
        predictions[mode] = predicted
    summary = {"torch":str(torch.__version__), "device":"cpu", "threads":1, "pretraining":source_summary, "target_seed":42, "target_train_rows":120, "target_test_rows":200, "target_epochs":20, "target_batch_size":32, "initial_target_heads_identical":all(all(torch.equal(v, head[k]) for k,v in initial_heads[0].items()) for head in initial_heads[1:]), "test_used_for_training_or_selection":False, "target_classes":["even","odd"], "experiments":records}
    (results / "comparison-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    write_csv(results / "comparison.csv", [{"mode":r["mode"],"train_correct":r["train"]["correct"],"test_correct":r["test"]["correct"],"test_rows":200,"accuracy":r["test"]["accuracy"],"loss":r["test"]["loss"],"target_updates":r["updates"],"target_seconds":r["seconds"]} for r in records])
    write_csv(results / "target-history.csv", [{"mode":m,**row} for m,h in histories.items() for row in h])
    write_csv(results / "pretraining-history.csv", source_history)
    write_csv(results / "test-predictions.csv", [{"source_id":row["source_id"],"digit":row["digit"],"true_parity":int(test_y[i]),**{m:int(p[i]) for m,p in predictions.items()}} for i,row in enumerate(test_rows)])
    draw_convolution(assets)
    draw_transfer(assets)
    fig, ax = new_figure("相同目标划分与20轮预算下的测试结果", "训练方式", "准确率（%）", "目标测试200张；单次固定种子结果；迁移另用了1000张源图片和30轮预训练")
    values = [100*r["test"]["correct"]/200 for r in records]
    ax.bar(list(LABELS.values()), values, color=["#5379b5","#38966c","#db8a32"],width=.6)
    ax.set_ylim(0,110)
    for i, (value, record) in enumerate(zip(values,records)):
        ax.text(i,value+2,f"{record['test']['correct']}/200\n{value:.1f}%",ha="center",fontsize=16)
    save_figure(fig,assets,"comparison")
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
