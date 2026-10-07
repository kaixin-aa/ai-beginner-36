from pathlib import Path

try:
    text = Path(__file__).with_name("not_created.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    print("找不到输入文件，请检查路径")
else:
    print(text)
