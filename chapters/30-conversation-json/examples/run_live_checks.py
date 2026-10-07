"""六个短真实需求的验收入口，所有用量读取平台响应。"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from plan_assistant import APIError, Config, live_chat
from plan_core import PlanError, empty_session, load_session, make_plan, save_session

ROOT = Path(__file__).resolve().parents[1]


def run():
    config = Config.from_env()
    chat = live_chat(config)
    cases = json.loads((ROOT / "data/teaching-cases.json").read_text(encoding="utf-8"))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    folder = ROOT / "results"
    folder.mkdir(exist_ok=True)
    path = folder / ("live-case-results-"+stamp+".json")
    session_path = folder / ("live-validation-session-"+stamp+".json")
    result = {"kind": "live_api", "date": datetime.now(timezone(timedelta(hours=8))).isoformat(),
              "provider": config.provider, "requested_model": config.model,
              "cases": [], "multiturn": None, "complete": False}
    first_state = None
    try:
        for index, case in enumerate(cases):
            state, attempts = make_plan(empty_session(), case["input"], case["daily_minutes"], chat)
            result["cases"].append({"input": case["input"], "daily_minutes": case["daily_minutes"],
                                    "plan": state["last_plan"], "attempts": attempts, "valid": True})
            if index == 0:
                first_state = state
            print("真实输入", index+1, "校验通过，预算", case["daily_minutes"], "请求次数", len(attempts))
        save_session(session_path, first_state)
        restored = load_session(session_path)
        updated, attempts = make_plan(restored, "改成10分钟，保留动手代码练习", 10, chat)
        save_session(session_path, updated)
        result["multiturn"] = {"before": first_state, "after": updated, "attempts": attempts,
                               "save_load_equal": restored == first_state, "session": session_path.name}
        result["complete"] = len(result["cases"]) == 5 and result["multiturn"]["save_load_equal"]
        all_attempts = [attempt for case in result["cases"] for attempt in case["attempts"]]+attempts
        result["request_count"] = len(all_attempts)
        result["total_tokens"] = sum(item["response"]["usage"]["total_tokens"] for item in all_attempts)
        print("多轮修改通过，真实请求合计", result["request_count"], "Token", result["total_tokens"])
    except (APIError, PlanError) as error:
        result["error"] = str(error)
        raise
    finally:
        with path.open("x", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
            file.write("\n")
        print("真实验证记录", path)


if __name__ == "__main__":
    run()
