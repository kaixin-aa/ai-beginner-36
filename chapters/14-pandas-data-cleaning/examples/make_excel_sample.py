"""由原始 CSV 生成内容一致的 Excel 教学副本。"""
from pathlib import Path
import pandas as pd

chapter = Path(__file__).resolve().parents[1]
raw = pd.read_csv(chapter / "data/raw_records.csv", dtype="string", keep_default_na=False)
raw.to_excel(chapter / "data/raw_records.xlsx", index=False, engine="openpyxl")
print("Excel 教学副本已生成，共", len(raw), "行")
