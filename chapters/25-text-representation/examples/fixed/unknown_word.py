import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from text_core import load_data, tokenize_words
print(tokenize_words("电脑",load_data()["vectors"]))
print("任意新文字可先查看字符切分",list("量子"))
print("字符切分成功不代表已拥有它们的向量")
