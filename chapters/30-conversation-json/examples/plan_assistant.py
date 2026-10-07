"""真实 API 对话入口，明确依赖第29章客户端。"""
import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = ROOT.parent / "29-first-api" / "examples"
sys.path.insert(0, str(DEPENDENCY))
from api_client import APIError, Config, ask
from plan_core import PlanError, load_session, make_plan, save_session


@dataclass
class ConversationRequest:
    base: Config
    messages: list

    def __getattr__(self, name):
        return getattr(self.base, name)

    def payload(self, question):
        body = self.base.payload(question)
        body["messages"] = self.messages
        body["response_format"] = {"type": "json_object"}
        return body


def live_chat(config):
    def chat(messages):
        current = messages[-1]["content"]
        return ask(ConversationRequest(config, messages), current)
    return chat


def main(argv=None):
    parser = argparse.ArgumentParser(description="带历史和JSON校验的学习计划助手")
    parser.add_argument("question")
    parser.add_argument("--minutes", type=int, help="明确当前时间预算，默认沿用会话预算")
    parser.add_argument("--session", type=Path, default=ROOT / "results/live-session.json")
    parser.add_argument("--repair", type=int, choices=(0, 1), default=1, help="最多一次格式修复，可能额外调用一次")
    args = parser.parse_args(argv)
    try:
        state = load_session(args.session)
        minutes = args.minutes if args.minutes is not None else state["daily_minutes"]
        config = Config.from_env()
        updated, attempts = make_plan(state, args.question, minutes, live_chat(config), retry_limit=args.repair)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        record_path = ROOT / "results" / ("live-turn-" + stamp + ".json")
        record_path.parent.mkdir(exist_ok=True)
        record = {"kind": "live_api", "recorded_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
                  "question": args.question, "daily_minutes": minutes, "attempts": attempts,
                  "plan": updated["last_plan"]}
        with record_path.open("x", encoding="utf-8") as file:
            json.dump(record, file, ensure_ascii=False, indent=2)
            file.write("\n")
        save_session(args.session, updated)
        print(json.dumps(updated["last_plan"], ensure_ascii=False, indent=2))
        print("实际请求次数", len(attempts))
        total = sum(item["response"]["usage"]["total_tokens"] for item in attempts)
        print("本轮所有尝试合计 Token", total)
        print("会话已保存", args.session)
        print("本轮请求与用量记录", record_path)
        return 0
    except (APIError, PlanError) as error:
        print(error, file=sys.stderr)
        return 1
    except OSError:
        print("会话读取或保存失败，请检查路径与权限", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
