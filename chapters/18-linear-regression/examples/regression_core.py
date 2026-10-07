"""同一划分比较均值基线、单特征与多特征最小二乘回归。"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["symboling", "normalized_losses", "make", "fuel_type", "aspiration", "num_of_doors", "body_style", "drive_wheels", "engine_location", "wheel_base", "length", "width", "height", "curb_weight", "engine_type", "num_of_cylinders", "engine_size", "fuel_system", "bore", "stroke", "compression_ratio", "horsepower", "peak_rpm", "city_mpg", "highway_mpg", "price"]
FEATURES = ["engine_size", "curb_weight", "horsepower"]
MODEL_FEATURES = {"baseline": ["engine_size"], "single": ["engine_size"], "multi": FEATURES}


def prepare_data(path=None):
    path = Path(path) if path is not None else ROOT / "data/imports-85.data"
    frame = pd.read_csv(path, header=None, na_values="?")
    if len(frame.columns) != len(COLUMNS):
        raise ValueError("原始文件必须有 26 列")
    frame.columns = COLUMNS
    frame.insert(0, "source_row", np.arange(1, len(frame)+1))
    frame.insert(0, "sample_id", [f"auto-{i:03d}" for i in range(len(frame))])
    required = [*FEATURES, "price"]
    for name in required:
        frame[name] = pd.to_numeric(frame[name], errors="raise")
    reasons = frame[required].isna().apply(lambda row: ",".join(row.index[row.to_numpy()].tolist()), axis=1)
    rejected = frame.loc[reasons != "", ["sample_id", "source_row", "make", *required]].copy()
    rejected["missing_fields"] = reasons[reasons != ""]
    clean = frame.loc[reasons == "", ["sample_id", "source_row", "make", *required]].copy()
    if len(clean) < 5:
        raise ValueError("完整记录不足，无法进行本章划分")
    values = clean[required].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("本章要求特征与价格均为有限正数")
    summary = {"raw_rows": len(frame), "complete_rows": len(clean), "rejected_rows": len(rejected), "missing_counts_in_selected_fields": frame[required].isna().sum().astype(int).to_dict(), "policy": "只删除本章所选特征或价格缺失的行，未填补标签；保留拒绝表", "selected_features": FEATURES}
    return clean, rejected, summary


def split_data(clean):
    train, test = train_test_split(clean, test_size=0.2, random_state=42)
    assert set(train.sample_id).isdisjoint(test.sample_id)
    return train.copy(), test.copy()


def metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if actual.ndim != 1 or predicted.shape != actual.shape or len(actual) < 2:
        raise ValueError("真实值与预测值须是至少两项的等长一维数组")
    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("指标输入必须是有限数值")
    return {"MAE": float(mean_absolute_error(actual, predicted)), "RMSE": float(root_mean_squared_error(actual, predicted)), "R2": float(r2_score(actual, predicted))}


def run_experiment(clean=None):
    if clean is None:
        clean, _, _ = prepare_data()
    train, test = split_data(clean)
    models = {"baseline": DummyRegressor(strategy="mean"), "single": LinearRegression(), "multi": LinearRegression()}
    scores = {}
    checked = test.copy()
    for name, model in models.items():
        fields = MODEL_FEATURES[name]
        model.fit(train[fields], train["price"])
        pred_train = model.predict(train[fields])
        pred_test = model.predict(test[fields])
        scores[name] = {"features": fields, "train": metrics(train["price"], pred_train), "test": metrics(test["price"], pred_test)}
        checked[f"{name}_prediction"] = pred_test
        checked[f"{name}_residual"] = test["price"].to_numpy()-pred_test
        checked[f"{name}_absolute_error"] = np.abs(checked[f"{name}_residual"])
    parameters = {name: {"intercept": float(models[name].intercept_), "coefficients": dict(zip(MODEL_FEATURES[name], models[name].coef_.tolist()))} for name in ["single", "multi"]}
    parameters["baseline"] = {"constant": float(models["baseline"].constant_[0, 0])}
    summary = {"random_state": 42, "test_size": 0.2, "train_rows": len(train), "test_rows": len(test), "scores": scores, "parameters": parameters, "worst_multi_test_rows": checked.sort_values("multi_absolute_error", ascending=False).head(5).to_dict("records"), "test_price_range": [float(test.price.min()), float(test.price.max())], "train_feature_ranges": {field: [float(train[field].min()), float(train[field].max())] for field in FEATURES}, "negative_multi_predictions": int((checked.multi_prediction < 0).sum())}
    return models, train, checked, summary
