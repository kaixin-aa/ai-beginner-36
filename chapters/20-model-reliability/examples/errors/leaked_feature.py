import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from examples.evaluation_core import leakage_experiment
r=leakage_experiment()
print('含答案列的测试准确率',r['leaked_test_accuracy'])
assert r['leaked_features']==r['clean_features'],'检查失败，特征包含预测时拿不到的答案'
