import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collect_results import collect_usage
rows=collect_usage()
print('真实请求',len(rows),'Token',sum(r['total_tokens']for r in rows))
