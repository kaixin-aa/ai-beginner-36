from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_core import load_single_image, ROOT

image = load_single_image(ROOT / "data/sample-digit.png")
print("输入形状", tuple(image.shape))
