from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api_client import Config, ask
from local_fixture import FIXTURE_KEY, fixture_server
with fixture_server(status=429) as (base, _):
    ask(Config(base_url=base, api_key=FIXTURE_KEY, fixture_http=True), "问题")
