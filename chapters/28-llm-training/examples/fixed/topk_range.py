import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training_core import load_baseline,generate
model,tokenizer = load_baseline()
result = generate(model,tokenizer,"小猫",greedy=False,temperature=2,top_k=2,seed=7)
print(result["text"],result["stop_reason"])
