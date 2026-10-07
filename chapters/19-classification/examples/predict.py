import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import joblib
from examples.classification_core import ROOT,predict_one_with_proba

parser=argparse.ArgumentParser(description='依次输入萼片长宽与花瓣长宽，单位厘米')
parser.add_argument('values',type=float,nargs=4)
args=parser.parse_args()
try:
    file=ROOT/'results/model.joblib'
    meta=json.loads((ROOT/'results/classification-summary.json').read_text(encoding='utf-8'))
    if hashlib.sha256(file.read_bytes()).hexdigest()!=meta['model_sha256']:
        raise ValueError('模型校验不一致，请重新训练')
    result=predict_one_with_proba(joblib.load(file),args.values)
except (FileNotFoundError,ValueError) as error:
    parser.exit(2,str(error)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
