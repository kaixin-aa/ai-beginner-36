from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api_client import Config
from local_fixture import FIXTURE_KEY
Config(api_key=FIXTURE_KEY, max_tokens=-1).payload("问题")
