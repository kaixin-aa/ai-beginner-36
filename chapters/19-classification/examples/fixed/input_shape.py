import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from examples.classification_core import experiment,predict_one_with_proba
model,*_=experiment()
print(predict_one_with_proba(model,[5.1,3.5,1.4,.2]))
