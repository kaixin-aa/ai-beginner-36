import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from examples.classification_core import experiment
model,*_=experiment()
print(model.predict([5.1,3.5,1.4,.2]))
