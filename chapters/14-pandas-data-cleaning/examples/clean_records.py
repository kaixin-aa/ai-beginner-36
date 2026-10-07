"""教学记录清洗。保留未知时长，记录全部丢弃原因。"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

FIELDS = ["record_id", "title", "done", "minutes", "tag"]


def clean_records(raw):
    missing = set(FIELDS) - set(raw.columns)
    if missing:
        raise ValueError(f"缺少列 {sorted(missing)}")
    frame = raw[FIELDS].copy()
    for field in FIELDS:
        frame[field] = frame[field].astype("string").fillna("").str.strip()
    frame["record_id"] = frame["record_id"].str.upper()
    frame["done"] = frame["done"].str.lower()
    frame["tag"] = frame["tag"].str.lower()
    # 当前 CSV 没有单元格内换行，source_row 对应原文件物理行号。
    frame["source_row"] = np.arange(2, len(frame) + 2)
    raw_missing = int(frame["minutes"].eq("").sum())
    duplicate_mask = frame.duplicated(subset=FIELDS, keep="first")
    duplicates = frame.loc[duplicate_mask].copy()
    frame = frame.loc[~duplicate_mask].copy()

    minute_text = frame["minutes"].copy()
    numeric = pd.to_numeric(minute_text, errors="coerce").astype("Float64")
    invalid_text = minute_text.ne("") & numeric.isna()
    frame["minutes_status"] = "known"
    frame.loc[minute_text.eq(""), "minutes_status"] = "missing"
    frame.loc[invalid_text, "minutes_status"] = "invalid_text"
    frame["minutes"] = numeric
    frame["done"] = frame["done"].map({"true": True, "false": False}).astype("boolean")

    conflicts = frame["record_id"].duplicated(keep=False)
    invalid_minutes = numeric.notna() & ((numeric < 0) | (numeric > 1440) | ~np.isfinite(numeric))
    reasons = pd.Series("", index=frame.index, dtype="string")
    for mask, reason in [
        (frame["record_id"].eq(""), "缺少记录 ID"),
        (frame["title"].eq(""), "标题为空"),
        (frame["done"].isna(), "完成状态非法"),
        (conflicts, "同一 ID 存在冲突记录"),
        (invalid_minutes.fillna(False), "分钟数必须是 0 到 1440 的有限数字"),
    ]:
        reasons.loc[mask] = reasons.loc[mask] + reason + "；"
    rejected = frame.loc[reasons.ne("")].copy()
    rejected["reason"] = reasons.loc[rejected.index].str.rstrip("；")
    clean = frame.loc[reasons.eq("")].copy()
    clean = clean.sort_values("record_id").reset_index(drop=True)
    audit = {
        "input_rows": len(raw),
        "duplicate_rows": len(duplicates),
        "rejected_rows": len(rejected),
        "output_rows": len(clean),
        "raw_missing_minutes": raw_missing,
        "invalid_minute_text_after_dedup": int(invalid_text.sum()),
        "clean_missing_minutes": int(clean["minutes"].isna().sum()),
        "known_minutes_count": int(clean["minutes"].notna().sum()),
        "known_minutes_total": float(clean["minutes"].sum()),
        "completed_rows": int(clean["done"].sum()),
    }
    assert audit["input_rows"] == audit["duplicate_rows"] + audit["rejected_rows"] + audit["output_rows"]
    return clean, duplicates, rejected, audit


def main():
    chapter = Path(__file__).resolve().parents[1]
    raw = pd.read_csv(chapter / "data/raw_records.csv", dtype="string", keep_default_na=False)
    excel = pd.read_excel(chapter / "data/raw_records.xlsx", dtype="string", keep_default_na=False, engine="openpyxl")
    if not raw.equals(excel):
        raise AssertionError("CSV 与 Excel 教学输入不一致")
    clean, duplicates, rejected, audit = clean_records(raw)
    results = chapter / "results"
    results.mkdir(exist_ok=True)
    clean.to_csv(results / "clean_records.csv", index=False, encoding="utf-8")
    duplicates.to_csv(results / "duplicate_records.csv", index=False, encoding="utf-8")
    rejected.to_csv(results / "rejected_records.csv", index=False, encoding="utf-8")
    (results / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"原始 {len(raw)} 行，重复 {len(duplicates)} 行，拒绝 {len(rejected)} 行，保留 {len(clean)} 行")
    print(f"分钟数原始缺失 {audit['raw_missing_minutes']} 个，清洗后缺失 {audit['clean_missing_minutes']} 个")
    print(f"已知分钟数合计 {audit['known_minutes_total']:g}，不含缺失值")
    print("CSV 与 Excel 输入一致", raw.equals(excel))
    print(clean[["record_id", "title", "done", "minutes", "minutes_status"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
