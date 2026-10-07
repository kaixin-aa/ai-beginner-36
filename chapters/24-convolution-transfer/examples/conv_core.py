"""轻量卷积预训练与新标签任务，手算卷积独立核对。"""
import csv
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
TEACHING_IMAGE = np.array([[1, 0, 2, 0], [0, 3, 0, 1], [1, 0, 2, 0], [0, 1, 0, 2]], dtype=np.float32)
TEACHING_KERNEL = np.array([[1, 0], [0, -1]], dtype=np.float32)


def manual_correlation(image, kernel):
    image, kernel = np.asarray(image), np.asarray(kernel)
    if image.ndim != 2 or kernel.ndim != 2 or any(a < b for a, b in zip(image.shape, kernel.shape)):
        raise ValueError("输入须为二维，卷积核不能大于图片")
    kh, kw = kernel.shape
    result = np.empty((image.shape[0]-kh+1, image.shape[1]-kw+1), dtype=np.float32)
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            result[row, col] = (image[row:row+kh, col:col+kw] * kernel).sum()
    return result


def load_manifest():
    data = ROOT / "data"
    metadata = json.loads((data / "source-metadata.json").read_text(encoding="utf-8"))
    if hashlib.sha256((data / "original-digits.npz").read_bytes()).hexdigest() != metadata["original_sha256"]:
        raise ValueError("原始快照哈希不一致")
    with (data / "split-manifest.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    if len(rows) != 1797 or sorted(int(row["source_id"]) for row in rows) != list(range(1797)):
        raise ValueError("角色清单必须唯一覆盖原编号")
    for role, count in {"pretrain": 1000, "target_train": 120, "target_test": 200, "unused": 477}.items():
        if sum(row["role"] == role for row in rows) != count:
            raise ValueError("数据角色数量不一致")
    return rows


class ParityImages(Dataset):
    def __init__(self, role):
        if role not in ["target_train", "target_test"]:
            raise ValueError("请选择目标训练或测试角色")
        self.rows = [row for row in load_manifest() if row["role"] == role]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        row = self.rows[index]
        path = ROOT / "data" / row["file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("图片哈希不一致")
        with Image.open(path) as image:
            if image.mode != "L" or image.size != (8, 8):
                raise ValueError("仅接受8×8灰度PNG")
            pixels = np.rint(np.asarray(image).astype(np.float32) * 16/255)/16
        label = int(row["target_label"])
        if label != int(row["digit"]) % 2:
            raise ValueError("奇偶标签映射不一致")
        return torch.from_numpy(pixels).unsqueeze(0), label


class TinyCNN(nn.Module):
    def __init__(self, classes=2):
        super().__init__()
        self.features = nn.Sequential(nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten(), nn.Linear(8*4*4, 32), nn.ReLU())
        self.head = nn.Linear(32, classes)

    def forward(self, images):
        return self.head(self.features(images))


def configure(seed):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(seed)


def freeze_features(model, frozen=True):
    for parameter in model.features.parameters():
        parameter.requires_grad_(not frozen)


def evaluate(model, x, y):
    model.eval()
    with torch.no_grad():
        scores = model(x)
        loss = nn.CrossEntropyLoss()(scores, y).item()
        prediction = scores.argmax(1)
    correct = int((prediction == y).sum())
    return {"loss": loss, "correct": correct, "rows": len(y), "accuracy": correct/len(y)}, prediction.numpy()


def fit(model, x, y, epochs, seed, mode="scratch", batch_size=32, learning_rate=0.01):
    if epochs < 1 or batch_size < 1 or not np.isfinite(learning_rate) or learning_rate <= 0:
        raise ValueError("训练参数须为有效正数")
    if mode not in ["scratch", "frozen", "fine_tune"]:
        raise ValueError("未知训练方式")
    loader = DataLoader(TensorDataset(x, y), batch_size=batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed), num_workers=0)
    freeze_features(model, mode != "scratch")
    started = perf_counter()
    optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=learning_rate)
    history, updates = [], 0
    for epoch in range(1, epochs+1):
        # 前10轮仅训练新分类头，后10轮全部微调；切换时重建优化器以纳入解冻参数。
        if mode == "fine_tune" and epoch == 11:
            freeze_features(model, False)
            optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
        model.train()
        for batch_x, batch_y in loader:
            optimizer.zero_grad(set_to_none=True)
            loss = nn.CrossEntropyLoss()(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
            updates += 1
        metric, _ = evaluate(model, x, y)
        history.append({"epoch": epoch, "train_loss": metric["loss"], "train_accuracy": metric["accuracy"]})
    return history, {"epochs": epochs, "updates": updates, "batch_size": batch_size, "learning_rate": learning_rate, "seconds": perf_counter()-started, "mode": mode}


def pretrain():
    configure(7)
    rows = load_manifest()
    ids = np.array([int(row["source_id"]) for row in rows if row["role"] == "pretrain"])
    with np.load(ROOT / "data/original-digits.npz", allow_pickle=False) as data:
        x = torch.tensor(data["images"][ids]/16, dtype=torch.float32).unsqueeze(1)
        y = torch.tensor(data["labels"][ids], dtype=torch.long)
    model = TinyCNN(10)
    history, timing = fit(model, x, y, 30, 7, batch_size=64)
    train_metric, _ = evaluate(model, x, y)
    return model, history, {**timing, "seed": 7, "rows": len(ids), "classes": 10, "train": train_metric, "independent_source_test": False}


def stack_dataset(role):
    dataset = ParityImages(role)
    pairs = [dataset[index] for index in range(len(dataset))]
    return torch.stack([x for x, _ in pairs]), torch.tensor([y for _, y in pairs], dtype=torch.long), dataset.rows


def target_model(mode, pretrained):
    configure(42)
    model = TinyCNN(2)
    if mode in ["frozen", "fine_tune"]:
        model.features.load_state_dict(pretrained.features.state_dict())
    elif mode != "scratch":
        raise ValueError("未知目标模型")
    return model


def save_target(model, path, mode):
    torch.save({"state_dict": model.state_dict(), "architecture": "conv8-pool-linear32-head2", "class_names": ["even", "odd"], "mode": mode, "torch": str(torch.__version__), "pixel_rule": "rint(png*16/255)/16"}, path)


def load_target(path):
    payload = torch.load(path, map_location="cpu", weights_only=True)
    if payload["architecture"] != "conv8-pool-linear32-head2" or payload["class_names"] != ["even", "odd"] or payload["torch"] != str(torch.__version__) or payload["pixel_rule"] != "rint(png*16/255)/16":
        raise ValueError("模型元数据与本章不一致")
    model = TinyCNN(2)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model
