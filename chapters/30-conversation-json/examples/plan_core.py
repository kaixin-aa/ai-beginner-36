"""有界对话历史、JSON 解析、结构及业务校验、一次格式修复。"""
from copy import deepcopy
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SYSTEM = (
    "你是中文学习计划助手。只返回一个JSON对象，不要代码围栏或解释。"
    "字段必须且只能为goal、daily_minutes、tasks。goal为非空字符串。"
    "daily_minutes为当前指定的整数分钟预算。tasks为1至6项列表，每项只包含"
    "非空title和正整数minutes。所有任务分钟合计必须等于daily_minutes。"
    "根据最新用户要求修改计划，结合保留的对话历史。"
    '形状示例为{"goal":"Python","daily_minutes":20,"tasks":[{"title":"练习变量","minutes":20}]}。示例分钟由当前预算替换。'
)


class PlanError(ValueError):
    pass


def validate_plan(plan, daily_minutes=None):
    if not isinstance(plan, dict) or set(plan) != {"goal", "daily_minutes", "tasks"}:
        raise PlanError("顶层字段必须恰好为 goal、daily_minutes、tasks")
    if not isinstance(plan["goal"], str) or not plan["goal"].strip():
        raise PlanError("goal 必须是非空字符串")
    budget = plan["daily_minutes"]
    if type(budget) is not int or not 1 <= budget <= 180:
        raise PlanError("daily_minutes 必须是 1 至 180 的整数")
    if daily_minutes is not None and budget != daily_minutes:
        raise PlanError("daily_minutes 与当前预算不一致")
    tasks = plan["tasks"]
    if not isinstance(tasks, list) or not 1 <= len(tasks) <= 6:
        raise PlanError("tasks 必须包含 1 至 6 个任务")
    total = 0
    for task in tasks:
        if not isinstance(task, dict) or set(task) != {"title", "minutes"}:
            raise PlanError("每个任务必须恰好包含 title 和 minutes")
        if not isinstance(task["title"], str) or not task["title"].strip():
            raise PlanError("title 必须是非空字符串")
        if type(task["minutes"]) is not int or task["minutes"] <= 0:
            raise PlanError("minutes 必须是正整数，不能使用布尔值")
        total += task["minutes"]
    if total != budget:
        raise PlanError("任务分钟之和必须等于当前预算")
    return deepcopy(plan)


def parse_plan(text, daily_minutes):
    try:
        plan = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        raise PlanError("回答不是可解析的 JSON 对象") from None
    return validate_plan(plan, daily_minutes)


def validate_history(history):
    if not isinstance(history, list) or len(history) % 2:
        raise PlanError("保存的历史必须是完整的用户与助手消息对")
    for i, message in enumerate(history):
        role = "user" if i % 2 == 0 else "assistant"
        if (not isinstance(message, dict) or set(message) != {"role", "content"}
                or message["role"] != role or not isinstance(message["content"], str)
                or not message["content"].strip()):
            raise PlanError("保存的历史角色或内容无效")
        if role == "assistant":
            try:
                validate_plan(json.loads(message["content"]))
            except (json.JSONDecodeError, PlanError):
                raise PlanError("历史中的助手计划未通过校验") from None


def build_messages(history, question, daily_minutes, max_pairs=3, char_budget=2000):
    validate_history(history)
    if not isinstance(question, str) or not question.strip():
        raise PlanError("用户需求不能为空")
    if type(daily_minutes) is not int or not 1 <= daily_minutes <= 180:
        raise PlanError("当前分钟预算必须是 1 至 180 的整数")
    if type(max_pairs) is not int or max_pairs < 0 or type(char_budget) is not int or char_budget <= 0:
        raise PlanError("裁剪配置无效")
    system = {"role": "system", "content": SYSTEM + f"当前预算为{daily_minutes}分钟。"}
    current = {"role": "user", "content": question.strip()}
    kept = deepcopy(history[-2 * max_pairs:]) if max_pairs else []
    def characters():
        return sum(len(item["content"]) for item in [system, *kept, current])
    while kept and characters() > char_budget:
        del kept[:2]
    if characters() > char_budget:
        raise PlanError("系统要求和当前需求已超过字符预算，请缩短需求")
    return [system, *kept, current]


def empty_session():
    return {"version": 1, "history": [], "last_plan": None, "daily_minutes": 20}


def load_session(path):
    path = Path(path)
    if not path.exists():
        return empty_session()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if set(state) != {"version", "history", "last_plan", "daily_minutes"} or type(state["version"]) is not int or state["version"] != 1:
            raise PlanError("会话结构或版本不支持")
        if type(state["daily_minutes"]) is not int or not 1 <= state["daily_minutes"] <= 180:
            raise PlanError("会话中的分钟预算无效")
        validate_history(state["history"])
        if state["last_plan"] is None:
            if state["history"] or state["daily_minutes"] != 20:
                raise PlanError("空会话状态不一致")
        else:
            validate_plan(state["last_plan"], state["daily_minutes"])
            if not state["history"] or json.loads(state["history"][-1]["content"]) != state["last_plan"]:
                raise PlanError("最后计划和历史不一致")
    except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
        raise PlanError("会话文件损坏，未覆盖原文件") from None
    return state


def save_session(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # 临时文件只创建在目标目录，成功写完后替换会话文件。
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix="plan-session-", suffix=".tmp", dir=path.parent, delete=False) as file:
            temporary = Path(file.name)
            json.dump(state, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def make_plan(state, question, daily_minutes, chat, retry_limit=1):
    if type(retry_limit) is not int or not 0 <= retry_limit <= 1:
        raise PlanError("本章最多允许一次格式修复请求")
    messages = build_messages(state["history"], question, daily_minutes)
    attempts = []
    for index in range(retry_limit + 1):
        # 网络、认证、限流错误向外传递；这里只修复已经收到的格式错误。
        response = chat(deepcopy(messages))
        text = response["answer"]
        try:
            if not response.get("complete", False):
                raise PlanError("回答达到上限或未正常结束，请返回更短的完整 JSON")
            plan = parse_plan(text, daily_minutes)
        except PlanError as error:
            attempts.append({"attempt": index+1, "valid": False, "reason": str(error), "response": response})
            if index == retry_limit:
                raise PlanError(f"{len(attempts)} 次回答仍未通过校验，会话未更新。最后错误为 {error}") from None
            messages += [{"role": "assistant", "content": text[:400]},
                         {"role": "user", "content": f"请修复JSON。校验错误为{error}。当前预算{daily_minutes}分钟，只返回符合要求的对象。"}]
            # 修复也受字符预算约束，先移除旧的完整消息对，保留最新需求。
            while len(messages) > 4 and sum(len(item["content"]) for item in messages) > 2000:
                del messages[1:3]
            if sum(len(item["content"]) for item in messages) > 2000:
                raise PlanError("修复请求超过字符预算，会话未更新")
            continue
        attempts.append({"attempt": index+1, "valid": True, "response": response})
        canonical = json.dumps(plan, ensure_ascii=False, separators=(",", ":"))
        # 持久化只保留有效消息对，修复反馈不进入长期历史。
        new_history = deepcopy(messages[1:-1]) if index == 0 else deepcopy(build_messages(state["history"], question, daily_minutes)[1:-1])
        new_history += [{"role": "user", "content": question.strip()}, {"role": "assistant", "content": canonical}]
        updated = {"version": 1, "history": new_history[-6:], "last_plan": plan, "daily_minutes": daily_minutes}
        return updated, attempts
    raise AssertionError("不可达分支")
