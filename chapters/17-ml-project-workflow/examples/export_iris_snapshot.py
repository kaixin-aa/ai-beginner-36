"""从固定版本 scikit-learn 的本地公开数据导出快照，不访问网络。"""
import hashlib
import json
from pathlib import Path
import pandas as pd
import sklearn
from sklearn.datasets import load_iris

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm"]


def main():
    iris = load_iris()
    folder = ROOT / "data"
    folder.mkdir(exist_ok=True)
    frame = pd.DataFrame(iris.data, columns=FEATURES)
    frame.insert(0, "sample_id", [f"iris-{i:03d}" for i in range(len(frame))])
    frame["target"] = iris.target
    path = folder / "iris.csv"
    frame.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")
    metadata = {"source": "sklearn.datasets.load_iris", "scikit_learn_version": sklearn.__version__, "reference": "https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_iris.html", "original_repository": "https://archive.ics.uci.edu/dataset/53/iris", "features": FEATURES, "unit": "cm", "target_names": iris.target_names.tolist(), "rows": len(frame), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "modifications": ["字段改为明确的英文名称，增加从0计数的教学编号", "沿用scikit-learn修订的两个测量点，不等同于UCI早期文件"]}
    (folder / "snapshot-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("已导出公开 Iris 数据", len(frame), "条；SHA256", metadata["sha256"])


if __name__ == "__main__":
    main()
