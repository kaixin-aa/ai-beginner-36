"""从第23章快照生成自行定义的奇偶图片文件夹，编号分区互斥。"""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "data"
    folder.mkdir(exist_ok=True)
    previous = ROOT.parent / "23-image-classification/data"
    source_path = previous / "digits.npz"
    source_meta = json.loads((previous / "source-metadata.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == source_meta["sha256"]
    destination = folder / "original-digits.npz"
    shutil.copyfile(source_path, destination)
    with np.load(destination, allow_pickle=False) as data:
        images, digits = data["images"], data["labels"]
    roles = np.full(len(digits), "unused", dtype="<U12")
    generator = np.random.default_rng(2026)
    for digit in range(10):
        ids = generator.permutation(np.flatnonzero(digits == digit))
        roles[ids[:100]] = "pretrain"
        roles[ids[100:112]] = "target_train"
        roles[ids[112:132]] = "target_test"
    rows = []
    for source_id, (digit, role) in enumerate(zip(digits, roles)):
        label = int(digit) % 2
        name = "odd" if label else "even"
        relative, sha = "", ""
        if role.startswith("target_"):
            path = folder / role / name / f"digit_{source_id:04d}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(np.rint(images[source_id] * (255.0/16)).astype(np.uint8)).save(path)
            relative = path.relative_to(folder).as_posix()
            sha = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append({"source_id": source_id, "digit": int(digit), "role": str(role), "target_label": label, "file": relative, "sha256": sha})
    with (folder / "split-manifest.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata = {"created_on": "2026-10-03", "split_seed": 2026, "original_sha256": source_meta["sha256"], "original_rows": len(digits), "role_counts": {str(role): int((roles == role).sum()) for role in np.unique(roles)}, "target_mapping": {"0": "even", "1": "odd"}, "pretrain_task": "10 digit classes", "target_task": "even/odd", "preprocessing": "PNG 0..255 -> rint(pixel*16/255)/16", "license": "CC BY 4.0", "attribution": "Alpaydin, E., & Kaynak, C. (1998). Optical Recognition of Handwritten Digits. UCI. DOI 10.24432/C50P49"}
    (folder / "source-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(metadata["role_counts"])


if __name__ == "__main__":
    main()
