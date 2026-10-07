from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from retrieval import split_text
split_text("示例资料","demo.txt",4,4)
