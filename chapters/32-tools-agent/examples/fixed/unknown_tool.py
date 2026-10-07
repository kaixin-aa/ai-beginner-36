import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import dispatch
print(dispatch("calculate",{"expression":"3*(8+9)"},lambda _:None))
