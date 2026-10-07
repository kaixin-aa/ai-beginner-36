"""命令行只读取自己训练保存的本地模型，接收厘米单位的四个特征。"""
import argparse
from pathlib import Path
from model_io import load_model
from project_core import predict_one

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="Iris 单条预测，输入顺序为萼片长、萼片宽、花瓣长、花瓣宽，单位厘米")
    parser.add_argument("values", type=float, nargs=4)
    args = parser.parse_args()
    try:
        result = predict_one(load_model(ROOT / "results"), args.values)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    print(result["label"], result["name"])


if __name__ == "__main__":
    main()
