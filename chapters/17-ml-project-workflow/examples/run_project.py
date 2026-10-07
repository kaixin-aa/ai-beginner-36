"""一次执行训练、评估、保存、重载和结果导出。"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from project_core import FEATURES, load_dataset, train_project, predict_one
from model_io import save_model, load_model

ROOT = Path(__file__).resolve().parents[1]


def main():
    model, train, test, summary = train_project()
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    save_model(model, results)
    restored = load_model(results)
    assert np.array_equal(model.predict(test[FEATURES]), restored.predict(test[FEATURES]))
    train.to_csv(results / "train_rows.csv", index=False, lineterminator="\n")
    test.to_csv(results / "test_predictions.csv", index=False, lineterminator="\n")
    split = pd.concat([train[["sample_id"]].assign(split="train"), test[["sample_id"]].assign(split="test")])
    split.to_csv(results / "split_manifest.csv", index=False, lineterminator="\n")
    summary["dataset_sha256"] = hashlib.sha256((ROOT / "data/iris.csv").read_bytes()).hexdigest()
    summary["reload_predictions_identical"] = True
    summary["single_input"] = {"values": [5.1, 3.5, 1.4, 0.2], "unit": "cm", "purpose": "沿用公开数据首行的教学输入，非独立新样本", "prediction": predict_one(restored, [5.1, 3.5, 1.4, 0.2])}
    (results / "project-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"训练 {len(train)} 条，测试 {len(test)} 条")
    print("每类训练/测试", summary["train_class_counts"], summary["test_class_counts"])
    print(f"训练准确率 {summary['train_accuracy']:.4f}")
    print(f"测试正确 {summary['test_correct']}/{len(test)}，准确率 {summary['test_accuracy']:.4f}")
    print(f"基线测试准确率 {summary['baseline_test_accuracy']:.4f}")
    print("重载预测一致", summary["reload_predictions_identical"])
    print("单条教学输入", summary["single_input"]["prediction"])
    print("错误样本", test.loc[~test["correct"], ["sample_id", "target", "prediction"]].to_dict("records"))


if __name__ == "__main__":
    main()
