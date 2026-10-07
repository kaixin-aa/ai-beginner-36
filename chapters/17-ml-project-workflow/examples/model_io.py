"""只用于保存和读回本章自行训练的可信模型。哈希不代替来源信任。"""
import hashlib
import json
from pathlib import Path
import pickle
import sys
import numpy as np
import pandas as pd
import scipy
import sklearn
if __package__:
    from .project_core import FEATURES, TARGET_NAMES
else:
    from project_core import FEATURES, TARGET_NAMES


def versions():
    return {"python": ".".join(map(str, sys.version_info[:3])), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__, "scikit_learn": sklearn.__version__}


def save_model(model, folder):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    path = folder / "iris_pipeline.pkl"
    payload = {"model": model, "features": FEATURES, "target_names": TARGET_NAMES}
    path.write_bytes(pickle.dumps(payload, protocol=5))
    metadata = {"versions": versions(), "features": FEATURES, "target_names": TARGET_NAMES, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "trusted_local_artifact_only": True}
    (folder / "model-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_model(folder):
    # 调用者须确认来源可信。pickle 可以执行代码，以下校验仅发现损坏与环境不一致。
    folder = Path(folder)
    path = folder / "iris_pipeline.pkl"
    metadata = json.loads((folder / "model-metadata.json").read_text(encoding="utf-8"))
    if metadata["versions"] != versions():
        raise ValueError("环境版本不同，请在当前环境重新训练保存模型")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != metadata["sha256"]:
        raise ValueError("模型文件校验不一致，请重新运行训练程序")
    payload = pickle.loads(content)
    if payload["features"] != FEATURES or payload["target_names"] != TARGET_NAMES:
        raise ValueError("模型字段顺序或类别映射不一致")
    return payload["model"]
