"""按模型的训练字段预测，并验证长度。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from regression_core import run_experiment, MODEL_FEATURES

models, _, test, _ = run_experiment()
prediction = models["single"].predict(test[MODEL_FEATURES["single"]])
print("预测数量", len(prediction))
print("前三条预测", [round(value, 2) for value in prediction[:3]])
assert len(prediction) == len(test)
