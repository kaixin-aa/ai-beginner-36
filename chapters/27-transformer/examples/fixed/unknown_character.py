import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from toy_transformer import load_corpus,CharacterTokenizer
tokenizer = CharacterTokenizer.from_sentences(load_corpus()["sentences"])
print(tokenizer.encode("小猫",bos=True))
print("扩展词表还需调整并训练模型，不能只把未知字塞进输入")
