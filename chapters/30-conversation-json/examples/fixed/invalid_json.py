from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_core import empty_session, make_plan
from run_cases import TeachingReplay
replay = TeachingReplay(['```json\n{}\n```', '{"goal":"Python","daily_minutes":20,"tasks":[{"title":"改写变量示例","minutes":20}]}'])
state, attempts = make_plan(empty_session(), "学Python", 20, replay)
print("教学回应修复次数", len(attempts)-1)
print(state["last_plan"])
