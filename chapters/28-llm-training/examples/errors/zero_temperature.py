import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training_core import probabilities_at_temperature
print(probabilities_at_temperature([2,1,0],0))
