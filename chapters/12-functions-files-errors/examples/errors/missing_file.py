from pathlib import Path

Path(__file__).with_name("not_created.txt").read_text(encoding="utf-8")
