import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from toy_transformer import ROOT,load_model,generate
model,tokenizer = load_model(ROOT/"results/tiny-transformer.pt")
result = generate(model,tokenizer,"小猫",max_new_tokens=1)
print(result["text"],result["stop_reason"])
