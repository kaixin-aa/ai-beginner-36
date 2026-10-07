import json
from pathlib import Path
from agent import run_agent
from teaching_replay import Replay,tool_message,final_message
ROOT=Path(__file__).resolve().parents[1]


def run():
    responses=[tool_message("search_documents",{"query":"借阅期限"},"search_1"),
               tool_message("calculate",{"expression":"14+7"},"calc_1"),final_message()]
    def teaching_search(query):return {"hits":[{"source":"guide.md","text":"书籍借阅期限为14天，续借增加7天。"}]}
    client=Replay(responses)
    success=run_agent("借阅期限加续借是多少",client,teaching_search)
    blocked=run_agent("写文件",Replay([tool_message("write_file",{"path":"demo.txt"})]),teaching_search)
    repeated=run_agent("算数",Replay([tool_message("calculate",{"expression":"1+1"},"a"),tool_message("calculate",{"expression":"1+1"},"b")]),teaching_search)
    malformed=tool_message("calculate",{"expression":"1+1"});malformed["message"]["tool_calls"][0]["function"]["arguments"]="bad-json"
    invalid=run_agent("算数",Replay([malformed]),teaching_search)
    result={"kind":"teaching_replay","model_called":False,"success":success,"requests":client.requests,
            "blocked":blocked,"repeated":repeated,"invalid_arguments":invalid}
    output=ROOT/"results";output.mkdir(exist_ok=True)
    (output/"case-results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("教学回放",[(key,result[key]["status"])for key in("success","blocked","repeated","invalid_arguments")])


if __name__=="__main__":run()
