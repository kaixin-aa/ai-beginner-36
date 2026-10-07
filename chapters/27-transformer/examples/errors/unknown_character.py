import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from toy_transformer import load_corpus,CharacterTokenizer
tokenizer = CharacterTokenizer.from_sentences(load_corpus()["sentences"])
print(tokenizer.encode("火星"))
