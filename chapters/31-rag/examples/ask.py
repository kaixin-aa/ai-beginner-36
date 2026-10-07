import argparse
from datetime import datetime
import json
from pathlib import Path
from embedding import Embedder
from retrieval import load_index,search
from rag_answer import Config,live_chat,answer_from_hits
ROOT=Path(__file__).resolve().parents[1]


def main(argv=None):
    parser=argparse.ArgumentParser(description="检索本地教学资料并按来源回答")
    parser.add_argument("question")
    args=parser.parse_args(argv)
    encoder=Embedder()
    data,vectors=load_index(ROOT/"results/index",ROOT/"data/documents",encoder.revision)
    hits=search(data,vectors,encoder.encode([args.question],query=True)[0])
    # 查无资料时无需密钥，也不会调用模型。
    chat=live_chat(Config.from_env()) if hits else None
    result=answer_from_hits(args.question,hits,chat)
    print(result["status"],result["answer"])
    for citation in result["citations"]:
        print(citation["source"],f"第{citation['line_start']}至{citation['line_end']}行",citation["quote"])
    output=ROOT/"results"/("cli-rag-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")+".json")
    with output.open("x",encoding="utf-8")as file:
        json.dump({"question":args.question,"hits":hits,"result":result},file,ensure_ascii=False,indent=2)
        file.write("\n")
    print("记录",output)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
