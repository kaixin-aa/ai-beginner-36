import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from contracts_demo import FilePolicy
print(FilePolicy().validate('notes.txt',10))
