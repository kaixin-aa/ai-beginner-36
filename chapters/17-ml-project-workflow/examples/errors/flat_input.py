"""故意把一条四特征记录误写成一维数组。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_core import train_project

model, _, _, _ = train_project()
model.predict([5.1, 3.5, 1.4, 0.2])
