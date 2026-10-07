"""复用已生成的问题向量，只向平台发送需要回答的检索片段。"""
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
from rag_answer import Config,live_chat,answer_from_hits
ROOT=Path(__file__).resolve().parents[1]


def run():
    data=json.loads((ROOT/"results/retrieval-results.json").read_text(encoding="utf-8"))
    chat=live_chat(Config.from_env())
    records=[]
    for item in data["records"]:
        if item["split"]!="test":
            continue
        result=answer_from_hits(item["question"],item["hits"],chat)
        matched=result["status"]==item["expected"] and (not item.get("answer_contains") or item["answer_contains"] in result["answer"])
        records.append({"question":item["question"],"expected":item["expected"],"hits":item["hits"],"result":result,"expected_matched":matched})
        print(item["question"],result["status"],"预期一致",matched)
    totals=sum(item["result"]["usage"]["total_tokens"] for item in records if item["result"]["usage"])
    stamp=datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path=ROOT/"results"/("live-rag-"+stamp+".json")
    data={"kind":"live_api","date":datetime.now(timezone(timedelta(hours=8))).isoformat(),"records":records,
          "request_count":sum(item["result"]["model_called"] for item in records),"total_tokens":totals,
          "all_expected_matched":all(item["expected_matched"] for item in records)}
    with path.open("x",encoding="utf-8")as file:
        json.dump(data,file,ensure_ascii=False,indent=2)
        file.write("\n")
    print("真实请求",data["request_count"],"Token",totals,"记录",path)


if __name__=="__main__":
    run()
