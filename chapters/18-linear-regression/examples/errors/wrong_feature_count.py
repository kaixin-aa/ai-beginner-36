"""故意给单特征模型传入三个特征。"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from regression_core import run_experiment, FEATURES

models, _, test, _ = run_experiment()
models["single"].predict(test[FEATURES])
