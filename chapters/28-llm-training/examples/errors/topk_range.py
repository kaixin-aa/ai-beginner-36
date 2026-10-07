import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from training_core import load_baseline,generate
model,tokenizer = load_baseline()
print(generate(model,tokenizer,"小猫",top_k=100))
