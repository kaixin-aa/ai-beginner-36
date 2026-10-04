import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from attention_core import softmax_rows
print(softmax_rows([[0,-np.inf]]))
