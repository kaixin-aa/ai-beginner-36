from copy import deepcopy
import json


def tool_message(name,args,call_id="call_demo"):
    return {"message":{"role":"assistant","content":None,"tool_calls":[{"id":call_id,"type":"function","function":{"name":name,"arguments":json.dumps(args,ensure_ascii=False)}}]},
            "finish_reason":"tool_calls","usage":{"prompt_tokens":10,"completion_tokens":5,"total_tokens":15},"kind":"teaching_replay"}


def final_message(content="计算结果为21。"):
    return {"message":{"role":"assistant","content":content},"finish_reason":"stop",
            "usage":{"prompt_tokens":20,"completion_tokens":5,"total_tokens":25},"kind":"teaching_replay"}


class Replay:
    def __init__(self,responses):self.responses=list(responses);self.requests=[]
    def __call__(self,messages):
        self.requests.append(deepcopy(messages))
        return deepcopy(self.responses.pop(0))
