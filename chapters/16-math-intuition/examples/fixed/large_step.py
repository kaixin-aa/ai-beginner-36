"""缩小步长后重新计算，不沿用失败实验的参数。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from math_core import descent

rows = descent(9, 0.2, 1)
print("损失变化", [round(row["loss"], 2) for row in rows])
assert rows[1]["loss"] < rows[0]["loss"]
