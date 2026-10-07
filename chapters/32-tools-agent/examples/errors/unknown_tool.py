import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import dispatch
dispatch("write_file",{"path":"demo.txt"},lambda _:None)
