"""8×8 数字分类，统一像素规则、固定 CPU 训练、独立状态文件。"""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]


def load_snapshot():
    path = ROOT / "data/digits.npz"
    metadata = json.loads((ROOT / "data/source-metadata.json").read_text(encoding="utf-8"))
    if hashlib.sha256(path.read_bytes()).hexdigest() != metadata["sha256"]:
        raise ValueError("数据快照校验不一致，请恢复或重新导出")
    with np.load(path, allow_pickle=False) as data:
        images, labels, train, test = (data[key].copy() for key in ["images", "labels", "train_indices", "test_indices"])
    if images.shape != (1797, 8, 8) or labels.shape != (1797,):
        raise ValueError("快照形状不符合约定")
    if not np.isin(labels, np.arange(10)).all():
        raise ValueError("类别必须是0至9")
    if len(np.unique(np.concatenate([train, test]))) != len(labels) or set(train) & set(test):
        raise ValueError("训练测试编号必须无交集且覆盖全部记录")
    return images, labels, train, test


def pixels_to_tensor(images):
    values = np.asarray(images)
    if values.ndim == 2:
        values = values[None, :, :]
    if values.ndim != 3 or values.shape[1:] != (8, 8) or len(values) == 0:
        raise ValueError("需要非空的8×8像素矩阵或一批矩阵")
    if not np.isfinite(values).all() or (values < 0).any() or (values > 16).any():
        raise ValueError("原像素必须为0至16的有限数值")
    return torch.from_numpy(values.astype(np.float32) / 16).unsqueeze(1)


def load_single_image(path):
    path = Path(path)
    if path.suffix.lower() == ".npy":
        values = np.load(path, allow_pickle=False)
    elif path.suffix.lower() == ".png":
        with Image.open(path) as image:
            if image.mode != "L" or image.size != (8, 8):
                raise ValueError("PNG须为8×8单通道灰度图，请先确认尺寸与模式")
            # 快照 PNG 用0至255展示；恢复到数据原有0至16尺度再使用统一归一化。
            values = np.rint(np.asarray(image).astype(float) * 16 / 255)
    else:
        raise ValueError("本章入口仅支持PNG或NPY")
    if values.shape != (8, 8):
        raise ValueError("单图必须恰好是8×8矩阵")
    return pixels_to_tensor(values)


def make_model():
    return nn.Sequential(nn.Flatten(), nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))


def evaluate(model, features, labels):
    model.eval()
    with torch.no_grad():
        logits = model(features)
        loss = nn.CrossEntropyLoss()(logits, labels).item()
        prediction = logits.argmax(dim=1)
        correct = int((prediction == labels).sum().item())
    return {"loss": loss, "accuracy": correct/len(labels), "correct": correct, "rows": len(labels)}, prediction


def train_model(epochs=30, batch_size=64, learning_rate=0.01):
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in [epochs, batch_size]):
        raise ValueError("轮次和批量大小须为正整数")
    if not np.isfinite(learning_rate) or learning_rate <= 0:
        raise ValueError("学习率须为有限正数")
    torch.manual_seed(42)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    images, labels, train, test = load_snapshot()
    x, y = pixels_to_tensor(images), torch.from_numpy(labels).long()
    dataset = TensorDataset(x[train], y[train])
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0, drop_last=False, generator=torch.Generator().manual_seed(42))
    started = perf_counter()
    model = make_model()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()
    initial, _ = evaluate(model, x[train], y[train])
    history = [{"epoch": 0, "train_loss": initial["loss"], "train_accuracy": initial["accuracy"]}]
    steps = 0
    for epoch in range(1, epochs+1):
        model.train()
        for batch_x, batch_y in loader:
            optimizer.zero_grad(set_to_none=True)
            objective = loss_fn(model(batch_x), batch_y)
            objective.backward()
            optimizer.step()
            steps += 1
        current, _ = evaluate(model, x[train], y[train])
        history.append({"epoch": epoch, "train_loss": current["loss"], "train_accuracy": current["accuracy"]})
    trained, _ = evaluate(model, x[train], y[train])
    tested, prediction = evaluate(model, x[test], y[test])
    summary = {"seed": 42, "torch": str(torch.__version__), "device": "cpu", "threads": 1, "epochs": epochs, "batch_size": batch_size, "batches_per_epoch": len(loader), "last_batch_rows": len(train)%batch_size or batch_size, "optimizer_updates": steps, "learning_rate": learning_rate, "optimizer": "Adam", "parameters": sum(p.numel() for p in model.parameters()), "initial_train": initial, "final_train": trained, "test": tested, "train_class_counts": np.bincount(labels[train], minlength=10).tolist(), "test_class_counts": np.bincount(labels[test], minlength=10).tolist(), "training_seconds": perf_counter()-started, "test_used_for_training_or_selection": False, "data_sha256": hashlib.sha256((ROOT / "data/digits.npz").read_bytes()).hexdigest()}
    return model, images, labels, train, test, prediction.numpy(), history, summary


def save_model(model, path):
    payload = {"state_dict": model.state_dict(), "architecture": "flatten-64-32-relu-10", "input_shape": [1, 8, 8], "pixel_divisor": 16, "class_names": [str(i) for i in range(10)], "torch": str(torch.__version__)}
    torch.save(payload, path)


def load_model(path):
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if payload["architecture"] != "flatten-64-32-relu-10" or payload["pixel_divisor"] != 16 or payload["class_names"] != [str(i) for i in range(10)]:
        raise ValueError("模型结构或像素规则不一致")
    if payload["torch"] != str(torch.__version__):
        raise ValueError("版本不同，请按当前环境重新训练")
    model = make_model()
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model


def predict_image(model, image):
    if tuple(image.shape) != (1, 1, 8, 8):
        raise ValueError("单图张量须为1×1×8×8")
    model.eval()
    with torch.no_grad():
        probabilities = torch.softmax(model(image), dim=1)[0]
    label = int(probabilities.argmax().item())
    return {"label": label, "probabilities": probabilities.tolist()}
