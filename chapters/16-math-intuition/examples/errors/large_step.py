"""方向正确，过大的步长仍会增加损失。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from math_core import descent

rows = descent(9, 1.1, 1)
print("损失变化", [round(row["loss"], 2) for row in rows])
assert rows[1]["loss"] < rows[0]["loss"], "步长过大，跨过最低点后走得太远"
