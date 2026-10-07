import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training_core import probabilities_at_temperature
print(probabilities_at_temperature([2,1,0],.5).numpy().round(6))
print("需要确定性最高分时使用贪心选择，不将除数设为0")
