from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rag_answer import validate_answer
validate_answer('{"status":"answered","answer":"借30天","citations":[{"chunk_id":"不存在","quote":"借30天"}]}',[])
