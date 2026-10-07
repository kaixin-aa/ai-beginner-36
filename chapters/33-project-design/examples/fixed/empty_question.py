import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from contracts_demo import AskRequest
print(AskRequest('柳叶学习室周一开放吗？').question)
