"""三个问题使用同一份教学数据，明确记录有效样本数。"""
from pathlib import Path
import numpy as np
import pandas as pd

BINS = [0, 10, 20, 30, 40, 50]


def load_records(path):
    frame = pd.read_csv(path, dtype={"record_id": "string", "title": "string", "done": "boolean", "minutes": "Float64", "tag": "string"})
    required = {"record_id", "title", "done", "minutes", "tag"}
    if not required.issubset(frame.columns):
        raise ValueError("缺少必需列")
    if frame["done"].isna().any() or frame["tag"].isna().any():
        raise ValueError("完成状态与标签不能缺失")
    known = frame["minutes"].dropna().astype(float)
    if not np.isfinite(known).all() or ((known < 0) | (known > 1440)).any():
        raise ValueError("分钟数必须为 0 到 1440 的有限数字")
    return frame


def summarize(frame):
    known = frame.loc[frame["minutes"].notna()].copy()
    values = known["minutes"].to_numpy(dtype=float)
    histogram, edges = np.histogram(values, bins=BINS)
    if int(histogram.sum()) != len(values):
        raise ValueError("有已知时长落在直方图区间之外，请扩展 BINS")
    grouped = frame.groupby("tag", sort=True).agg(
        records=("record_id", "size"), completed=("done", "sum"),
        known_minutes=("minutes", "count"), known_total=("minutes", "sum"),
    )
    grouped["missing_minutes"] = grouped["records"] - grouped["known_minutes"]
    grouped["completion_rate"] = grouped["completed"] / grouped["records"]
    points = pd.DataFrame({"minutes": known["minutes"].astype(float), "done_code": known["done"].astype(int)})
    correlation = None
    if len(points) >= 2 and points["minutes"].nunique() > 1 and points["done_code"].nunique() > 1:
        correlation = float(points.corr(method="pearson").loc["minutes", "done_code"])
    return {
        "input_rows": len(frame), "known_minutes_rows": len(known),
        "missing_minutes_rows": int(frame["minutes"].isna().sum()),
        "known_total": float(values.sum()), "known_mean": float(values.mean()) if len(values) else None,
        "known_median": float(np.median(values)) if len(values) else None,
        "histogram_counts": histogram.tolist(), "histogram_edges": edges.tolist(),
        "groups": grouped.reset_index().to_dict("records"),
        "scatter_points": [
            {"record_id": str(row.record_id), "minutes": float(row.minutes), "done_code": int(row.done)}
            for row in known.itertuples()
        ],
        "pearson_r": correlation,
    }
