import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from examples.evaluation_core import leakage_experiment
r=leakage_experiment()
print('移除答案列的测试准确率',r['clean_test_accuracy'])
assert r['clean_features']==6
