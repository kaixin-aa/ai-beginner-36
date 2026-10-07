import argparse
from datetime import datetime
import json
from pathlib import Path
from agent import run_agent
from tool_client import Config,ToolClient,APIError
from tools import LocalSearch
ROOT=Path(__file__).resolve().parents[1]


def main(argv=None):
    parser=argparse.ArgumentParser(description="受控计算器与只读资料搜索助手")
    parser.add_argument("question")
    args=parser.parse_args(argv)
    try:
        local_search=LocalSearch()
        result=run_agent(args.question,ToolClient(Config.from_env()),local_search)
    except(ValueError,APIError,OSError)as error:
        print(error)
        return 1
    output=ROOT/"results"/("live-agent-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")+".json")
    output.parent.mkdir(exist_ok=True)
    with output.open("x",encoding="utf-8")as file:json.dump(result,file,ensure_ascii=False,indent=2)
    print(result["status"],result["answer"])
    print("模型请求",result["model_requests"],"工具执行",result["tool_count"],"Token",result["total_tokens"],"记录",output)
    return 0 if result["status"]=="completed"else 1


if __name__=="__main__":raise SystemExit(main())
