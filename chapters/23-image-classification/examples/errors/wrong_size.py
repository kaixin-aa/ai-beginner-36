from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from image_core import pixels_to_tensor

pixels_to_tensor(np.zeros((28, 28)))
