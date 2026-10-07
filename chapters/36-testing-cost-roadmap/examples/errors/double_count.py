import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collect_results import collect_usage
actual=sum(r['total_tokens']for r in collect_usage())
wrong=actual+4535  # 将离线核对保存的原用量重复加了一次。
print('错误合计',wrong)
assert wrong==5080,'离线核对不是新增模型请求，不能重复计入原用量'
