import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from text_core import cosine
print(cosine([0,0],[1,0]))
