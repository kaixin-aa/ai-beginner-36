"""命令行入口，文本文件必须使用 UTF-8。"""
import argparse
import json
from pathlib import Path

from text_stats import count_words


def main():
    parser = argparse.ArgumentParser(description="统计英文词频并保存 JSON")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    if args.input_file.resolve() == args.output_file.resolve():
        print("输入与输出不能使用同一个文件")
        return 2
    try:
        text = args.input_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("找不到输入文件，请检查路径")
        return 2
    except UnicodeDecodeError:
        print("输入文件不是有效的 UTF-8，请按原编码打开后另存为 UTF-8")
        return 2
    except OSError as error:
        print(f"无法读取输入文件，{error}")
        return 2

    result = count_words(text)
    result["source_file"] = args.input_file.name
    try:
        with args.output_file.open("w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        print(f"无法保存结果，请检查输出目录和写入权限，{error}")
        return 2
    print(f"总词数 {result['total_words']}，不同词数 {result['unique_words']}")
    if not text.strip():
        print("文本为空，已保存零计数结果")
    elif result["total_words"] == 0:
        print("没有匹配到英文词，本程序没有执行中文分词")
    print(f"已保存 {args.output_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
