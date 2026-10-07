import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from text_core import load_data, tokenize_words
print(tokenize_words("量子",load_data()["vectors"]))
