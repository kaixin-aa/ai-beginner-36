import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api_client import Config
os.environ["AI_API_KEY_ENV"] = "AI_TEACHING_MISSING_KEY"
os.environ.pop("AI_TEACHING_MISSING_KEY", None)
Config.from_env()
