"""保持特征、标签、编号配对，训练阶段只接触训练行。"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm"]
TARGET_NAMES = ["setosa", "versicolor", "virginica"]


def validate_frame(frame):
    required = ["sample_id", *FEATURES, "target"]
    if not set(required).issubset(frame.columns):
        raise ValueError("数据缺少编号、特征或标签字段")
    if len(frame) == 0:
        raise ValueError("数据不能为空")
    if frame["sample_id"].isna().any() or frame["sample_id"].duplicated().any():
        raise ValueError("样本编号不能为空或重复")
    x = frame[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(x).all() or (x <= 0).any():
        raise ValueError("四个测量值必须是有限正数，单位为厘米")
    if not frame["target"].isin([0, 1, 2]).all():
        raise ValueError("标签必须属于 0、1、2")
    return frame[required].copy()


def load_dataset(path=None):
    path = Path(path) if path is not None else ROOT / "data/iris.csv"
    return validate_frame(pd.read_csv(path))


def split_dataset(frame, random_state=42):
    frame = validate_frame(frame)
    train, test = train_test_split(frame, test_size=0.2, random_state=random_state, stratify=frame["target"])
    assert set(train["sample_id"]).isdisjoint(test["sample_id"])
    return train.copy(), test.copy()


def make_model():
    return Pipeline([("scale", StandardScaler()), ("classifier", LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs"))])


def train_project(frame=None):
    frame = load_dataset() if frame is None else validate_frame(frame)
    train, test = split_dataset(frame)
    x_train, y_train = train[FEATURES], train["target"]
    x_test, y_test = test[FEATURES], test["target"]
    model = make_model()
    baseline = DummyClassifier(strategy="most_frequent")
    model.fit(x_train, y_train)
    baseline.fit(x_train, y_train)
    predictions = model.predict(x_test)
    baseline_predictions = baseline.predict(x_test)
    correct = int(np.sum(predictions == y_test.to_numpy()))
    summary = {"random_state": 42, "test_size": 0.2, "stratified": True, "train_rows": len(train), "test_rows": len(test), "train_class_counts": train["target"].value_counts().sort_index().tolist(), "test_class_counts": test["target"].value_counts().sort_index().tolist(), "train_accuracy": float(accuracy_score(y_train, model.predict(x_train))), "test_accuracy": float(accuracy_score(y_test, predictions)), "test_correct": correct, "test_wrong": len(test)-correct, "baseline_test_accuracy": float(accuracy_score(y_test, baseline_predictions)), "fit_rows_in_scaler": int(model.named_steps["scale"].n_samples_seen_), "features": FEATURES, "target_names": TARGET_NAMES}
    checked = test.copy()
    checked["prediction"] = predictions
    checked["baseline_prediction"] = baseline_predictions
    checked["correct"] = predictions == y_test.to_numpy()
    return model, train, checked, summary


def predict_one(model, values):
    if isinstance(values, dict):
        if set(values) != set(FEATURES):
            raise ValueError("按字段名输入时必须恰好提供四个测量字段")
        values = [values[name] for name in FEATURES]
    x = np.asarray(values, dtype=float)
    if x.shape != (4,) or not np.isfinite(x).all() or (x <= 0).any():
        raise ValueError("单条输入需要四个有限正数，顺序与训练一致，单位为厘米")
    frame = pd.DataFrame([x], columns=FEATURES)
    predicted = int(model.predict(frame)[0])
    return {"label": predicted, "name": TARGET_NAMES[predicted]}
