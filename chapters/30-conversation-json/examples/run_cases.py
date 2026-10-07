"""五组作者编制的回应及多轮、失败案例，验证程序而非模型能力。"""
from copy import deepcopy
import json
from pathlib import Path
from plan_core import empty_session, load_session, make_plan, save_session, PlanError

ROOT = Path(__file__).resolve().parents[1]


class TeachingReplay:
    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []

    def __call__(self, messages):
        self.requests.append(deepcopy(messages))
        if not self.replies:
            raise RuntimeError("教学回应用尽")
        reply = self.replies.pop(0)
        return {"kind": "teaching_replay", "answer": reply, "complete": True,
                "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}


def run():
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    cases = json.loads((ROOT / "data/teaching-cases.json").read_text(encoding="utf-8"))
    records = []
    for case in cases:
        replay = TeachingReplay([json.dumps(case["plan"], ensure_ascii=False)])
        state, attempts = make_plan(empty_session(), case["input"], case["daily_minutes"], replay)
        records.append({"input": case["input"], "daily_minutes": case["daily_minutes"],
                        "plan": state["last_plan"], "attempts": len(attempts), "valid": True,
                        "kind": "teaching_replay"})
    first = cases[0]
    smaller = {"goal": "入门 Python", "daily_minutes": 10, "tasks": [{"title": "改写变量示例", "minutes": 10}]}
    replay = TeachingReplay([json.dumps(first["plan"], ensure_ascii=False), json.dumps(smaller, ensure_ascii=False)])
    state, _ = make_plan(empty_session(), first["input"], 20, replay)
    path = results / "teaching-session.json"
    save_session(path, state)
    restored = load_session(path)
    updated, _ = make_plan(restored, "改成10分钟，保留动手代码练习", 10, replay)
    save_session(path, updated)
    assert replay.requests[1][1:3] == state["history"]
    failures = []
    for name, bad in (("invalid_json", "这是一份计划"), ("missing_field", '{"goal":"Python"}')):
        repair = TeachingReplay([bad, json.dumps(first["plan"], ensure_ascii=False)])
        fixed, attempts = make_plan(empty_session(), first["input"], 20, repair)
        failures.append({"case": name, "bad_response": bad, "repair_requests": repair.requests,
                         "attempts": attempts, "fixed_plan": fixed["last_plan"]})
    broken = TeachingReplay(["坏JSON", "还是坏JSON"])
    old = empty_session()
    snapshot = deepcopy(old)
    try:
        make_plan(old, first["input"], 20, broken)
    except PlanError as error:
        exhausted = {"error": str(error), "requests": len(broken.requests), "state_unchanged": old == snapshot}
    else:
        raise AssertionError("应在两次无效回答后失败")
    summary = {"kind": "teaching_replay", "model_called": False, "cases": records,
               "multiturn": {"before": state, "after": updated, "second_request": replay.requests[1],
                             "save_load_equal": restored == state},
               "failure_repairs": failures, "exhausted": exhausted}
    (results / "case-results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("五组教学输入校验通过，多轮历史保存重载一致，两类格式错误修复通过")
    print("固定回应未调用模型；连续失败最多两次，会话不变", exhausted["state_unchanged"])


if __name__ == "__main__":
    run()
