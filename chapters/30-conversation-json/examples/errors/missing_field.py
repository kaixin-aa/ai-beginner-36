from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_core import parse_plan
parse_plan('{"goal":"Python","daily_minutes":20}', 20)
