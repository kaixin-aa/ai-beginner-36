"""可选快照重建入口。库内置数据，无需网络下载。"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]


def main():
    digits = load_digits()
    images = digits.images.astype(np.uint8)
    labels = digits.target.astype(np.int64)
    train, test = train_test_split(np.arange(len(labels)), test_size=0.2, random_state=42, stratify=labels)
    folder = ROOT / "data"
    folder.mkdir(exist_ok=True)
    path = folder / "digits.npz"
    np.savez_compressed(path, images=images, labels=labels, train_indices=train, test_indices=test)
    sample_index = int(test[0])
    gray = np.rint(images[sample_index].astype(float) / 16 * 255).astype(np.uint8)
    Image.fromarray(gray).save(folder / "sample-digit.png")
    np.save(folder / "sample-digit.npy", images[sample_index], allow_pickle=False)
    metadata = {"exported_on": "2026-10-03", "loader": "sklearn.datasets.load_digits", "sklearn": sklearn.__version__, "reference": "https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_digits.html", "repository": "https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits", "citation": "Alpaydin, E. & Kaynak, C. (1998). Optical Recognition of Handwritten Digits. https://doi.org/10.24432/C50P49", "license": "CC BY 4.0", "rows": len(labels), "shape_per_image": [8, 8], "value_range": [0, 16], "class_counts": np.bincount(labels, minlength=10).tolist(), "train_rows": len(train), "test_rows": len(test), "seed": 42, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "sample_image": {"source_index": sample_index, "true_label": int(labels[sample_index]), "split": "test", "purpose": "公开测试记录的接口演示，非独立外部图片"}, "changes": ["保存库中1797条图片及标签，非UCI全部5620条", "新增教学训练测试划分与编号，固定种子42", "首条测试图片导出PNG灰度与原像素NPY"]}
    (folder / "source-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("图片快照", len(labels), "训练/测试", len(train), len(test), "演示标签", metadata["sample_image"])


if __name__ == "__main__":
    main()
