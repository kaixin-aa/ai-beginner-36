from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from retrieval import split_text
print([item["text"]for item in split_text("abcdefghij","demo.txt",6,2)])
