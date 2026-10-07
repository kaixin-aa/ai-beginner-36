from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_core import parse_plan
plan = parse_plan('{"goal":"Python","daily_minutes":20,"tasks":[{"title":"运行变量示例","minutes":20}]}', 20)
print("字段补齐，合计分钟", sum(task["minutes"] for task in plan["tasks"]))
