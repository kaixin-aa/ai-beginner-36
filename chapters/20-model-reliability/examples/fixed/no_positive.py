import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from examples.evaluation_core import binary_report
print(binary_report([0,1],[0,0]))
