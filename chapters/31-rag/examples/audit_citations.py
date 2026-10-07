"""对已取得的真实回答重新核对精确原文位置，不再次请求模型。"""
import json
from pathlib import Path
from rag_answer import validate_answer
ROOT=Path(__file__).resolve().parents[1]


def run():
    live=json.loads((ROOT/"results/live-rag-20261004-011026-845879.json").read_text(encoding="utf-8"))
    records=[]
    for record in live["records"]:
        if not record["result"]["model_called"]:
            continue
        result=validate_answer(record["result"]["response"]["answer"],record["hits"])
        for citation in result["citations"]:
            text=(ROOT/"data/documents"/citation["source"]).read_bytes().decode("utf-8-sig")
            assert text[citation["quote_start"]:citation["quote_end"]]==citation["quote"]
        records.append({"question":record["question"],"validated":result})
    output={"original_record":"live-rag-20261004-011026-845879.json","api_repeated":False,
            "citation_count":sum(len(item["validated"]["citations"])for item in records),"records":records}
    (ROOT/"results/citation-audit.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("真实回答引用精确位置核对通过",output["citation_count"])


if __name__=="__main__":run()
