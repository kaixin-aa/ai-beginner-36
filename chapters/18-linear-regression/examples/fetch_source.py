"""可选数据获取入口。正常训练使用已随章保存的官方原始文件。"""
import hashlib
from datetime import date
from io import BytesIO
import json
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

URL = "https://archive.ics.uci.edu/static/public/10/automobile.zip"
ROOT = Path(__file__).resolve().parents[1]


def main():
    with urlopen(URL, timeout=30) as response:
        content = response.read()
    folder = ROOT / "data"
    folder.mkdir(exist_ok=True)
    hashes = {}
    # 不展开任意压缩路径，只将所需文件的内容写入固定目标名。
    with ZipFile(BytesIO(content)) as archive:
        for filename in ["imports-85.data", "imports-85.names"]:
            candidates = [name for name in archive.namelist() if name.endswith("/"+filename) or name == filename]
            if len(candidates) != 1:
                raise ValueError(f"官方压缩包中的 {filename} 数量不符合预期")
            raw = archive.read(candidates[0])
            (folder / filename).write_bytes(raw)
            hashes[filename] = hashlib.sha256(raw).hexdigest()
    metadata = {"downloaded_on": date.today().isoformat(), "download_url": URL, "dataset_page": "https://archive.ics.uci.edu/dataset/10/automobile", "citation": "Schlimmer, J. (1985). Automobile [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5B01C", "license": "CC BY 4.0", "archive_sha256": hashlib.sha256(content).hexdigest(), "files_sha256": hashes, "raw_files_modified": False}
    (folder / "source-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("已保存 UCI 官方原始数据与说明", hashes)


if __name__ == "__main__":
    main()
