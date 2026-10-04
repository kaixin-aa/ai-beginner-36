"""独立预测脚本，不调用训练，不读取训练标签。"""
import argparse
from pathlib import Path
from image_core import load_model, load_single_image, predict_image, ROOT


def main():
    parser = argparse.ArgumentParser(description="8×8灰度手写数字预测")
    parser.add_argument("image", type=Path)
    parser.add_argument("--model", type=Path, default=ROOT / "results/digits-state.pt")
    args = parser.parse_args()
    try:
        result = predict_image(load_model(args.model), load_single_image(args.image))
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    print("预测数字", result["label"])
    print("按0至9顺序的概率", [round(v, 4) for v in result["probabilities"]])


if __name__ == "__main__":
    main()
