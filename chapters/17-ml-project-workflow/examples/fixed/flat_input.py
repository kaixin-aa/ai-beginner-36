"""使用统一入口，将一条输入整理为一行四列。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_core import train_project, predict_one

model, _, _, _ = train_project()
print(predict_one(model, [5.1, 3.5, 1.4, 0.2]))
