import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from text_core import cosine
try:
    print(cosine([0,0],[1,0]))
except ValueError as error:
    print(error)
    print("先补充有内容的表示，再计算",cosine([1,0],[1,0]))
