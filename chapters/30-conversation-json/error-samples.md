# 实际错误与修复结果

运行日期为 2026 年 10 月 4 日，错误退出码均为 1，修复退出码均为 0。

## invalid_json

[错误文件](./examples/errors/invalid_json.py) 与 [修复文件](./examples/fixed/invalid_json.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\30-conversation-json\examples\errors\invalid_json.py", line 5, in <module>
    parse_plan("```json\n{}\n```", 20)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\30-conversation-json\examples\plan_core.py", line 53, in parse_plan
    raise PlanError("回答不是可解析的 JSON 对象") from None
plan_core.PlanError: 回答不是可解析的 JSON 对象
```

修复输出如下。

```text
教学回应修复次数 1
{'goal': 'Python', 'daily_minutes': 20, 'tasks': [{'title': '改写变量示例', 'minutes': 20}]}
```

## missing_field

[错误文件](./examples/errors/missing_field.py) 与 [修复文件](./examples/fixed/missing_field.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\30-conversation-json\examples\errors\missing_field.py", line 5, in <module>
    parse_plan('{"goal":"Python","daily_minutes":20}', 20)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\30-conversation-json\examples\plan_core.py", line 54, in parse_plan
    return validate_plan(plan, daily_minutes)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\30-conversation-json\examples\plan_core.py", line 24, in validate_plan
    raise PlanError("顶层字段必须恰好为 goal、daily_minutes、tasks")
plan_core.PlanError: 顶层字段必须恰好为 goal、daily_minutes、tasks
```

修复输出如下。

```text
字段补齐，合计分钟 20
```
