"""修复更新方向，并核对新损失。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from math_core import loss, gradient

w = 9
new_w = w - 0.2 * gradient(w)
print(f"更新前 w={w} loss={loss(w):.2f}")
print(f"更新后 w={new_w:.2f} loss={loss(new_w):.2f}")
assert loss(new_w) < loss(w)
