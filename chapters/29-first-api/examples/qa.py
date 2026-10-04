"""命令行一次问答；输出记录仅包含公开提问、回答和用量。"""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
from api_client import APIError, Config, ask


def main(argv=None):
    parser = argparse.ArgumentParser(description="一次模型问答，默认连接 DeepSeek")
    parser.add_argument("question", nargs="?", help="省略时在终端输入问题")
    parser.add_argument("--fixture-http", action="store_true", help="只供本地 HTTP 教学服务")
    parser.add_argument("--output", type=Path, help="记录路径，拒绝覆盖已有文件")
    args = parser.parse_args(argv)
    try:
        config = Config.from_env(fixture_http=args.fixture_http)
        question = args.question if args.question is not None else input("请输入问题\n")
        folder = Path(__file__).resolve().parents[1] / "results"
        folder.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        kind = "local_fixture" if config.fixture_http else "live_api"
        output = args.output or folder / (kind + "-" + stamp + ".json")
        if output.exists():
            raise FileExistsError()
        result = ask(config, question)
        result["recorded_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
        # x 模式保护已有用户记录。
        with output.open("x", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
            file.write("\n")
        print("本地教学响应" if result["kind"] == "local_fixture" else "真实 API 响应")
        print(result["answer"])
        usage = result["usage"]
        print(f"输入 {usage['prompt_tokens']} Token，输出 {usage['completion_tokens']} Token，合计 {usage['total_tokens']} Token")
        print("结束原因", result["finish_reason"])
        if not result["complete"]:
            print("回答达到上限，可能被截断，不能当作完整答案")
        print("记录文件", output)
        return 0
    except (APIError, FileExistsError, EOFError) as error:
        message = "记录文件已存在，请换一个路径" if isinstance(error, FileExistsError) else str(error)
        print(message, file=sys.stderr)
        return 1
    except OSError:
        print("本地记录保存失败，请检查路径与权限", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
