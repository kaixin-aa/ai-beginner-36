import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rag_answer import validate_answer
hit={"chunk_id":"demo@0-7","source":"demo.txt","text":"书籍可以借14天。","line_start":1,"line_end":1}
text=json.dumps({"status":"answered","answer":"14天","citations":[{"chunk_id":hit["chunk_id"],"quote":hit["text"]}]},ensure_ascii=False)
print(validate_answer(text,[hit])["citations"])
