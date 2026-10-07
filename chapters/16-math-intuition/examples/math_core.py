"""二次损失的数值实验。数据与函数均为原创教学设定。"""
from math import isfinite
from numbers import Real


def finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value):
        raise ValueError(f"{name} 必须是有限实数")
    return float(value)


def loss(w):
    w = finite_number(w, "w")
    return (w - 3) ** 2 + 1


def gradient(w):
    w = finite_number(w, "w")
    return 2 * (w - 3)


def finite_difference(w, h=0.001):
    w = finite_number(w, "w")
    h = finite_number(h, "h")
    if h <= 0:
        raise ValueError("h 必须大于零")
    return (loss(w + h) - loss(w - h)) / (2 * h)


def descent(start=9, learning_rate=0.2, steps=12):
    w = finite_number(start, "start")
    learning_rate = finite_number(learning_rate, "learning_rate")
    if learning_rate <= 0:
        raise ValueError("learning_rate 必须大于零")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps 必须是非负整数")
    records = []
    for step in range(steps + 1):
        records.append({"step": step, "w": w, "loss": loss(w), "gradient": gradient(w)})
        if step < steps:
            w -= learning_rate * gradient(w)
            if not isfinite(w):
                raise ValueError("更新产生非有限值，请检查学习率和迭代次数")
    return records
