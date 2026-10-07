import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import calculate
# 仅送入受限解析器，不执行输入中的文件操作。
calculate("open('demo.txt','w')")
