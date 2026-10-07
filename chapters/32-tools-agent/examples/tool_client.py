"""支持工具调用的固定端点适配器，沿用第29章认证与错误规则。"""
import json
from pathlib import Path
import socket
import sys
import time
from urllib.error import HTTPError,URLError
from urllib.request import Request,build_opener
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"29-first-api/examples"))
from api_client import Config,APIError,HTTP_HINTS,NoRedirect,redact
from tools import DEFINITIONS


def parse_tool_response(data):
    try:
        choice=data["choices"][0]
        message=choice["message"]
        finish=choice["finish_reason"]
        usage={key:data["usage"][key]for key in("prompt_tokens","completion_tokens","total_tokens")}
        if any(type(v)is not int or v<0 for v in usage.values())or usage["total_tokens"]!=usage["prompt_tokens"]+usage["completion_tokens"]:
            raise ValueError()
        calls=message.get("tool_calls")or[]
        if not isinstance(calls,list)or finish not in("stop","tool_calls","length")or message.get("role")!="assistant":raise ValueError()
        if finish=="tool_calls"and not calls:raise ValueError()
        if finish=="stop"and(calls or not isinstance(message.get("content"),str)or not message["content"].strip()):raise ValueError()
        clean={key:message[key]for key in("role","content","tool_calls","reasoning_content")if key in message}
        return {"message":clean,"finish_reason":finish,"usage":usage,"response_id":data["id"],"returned_model":data["model"]}
    except(KeyError,IndexError,TypeError,ValueError):
        raise APIError("工具响应结构或用量无效")from None


class ToolClient:
    def __init__(self,config):self.config=config

    def __call__(self,messages):
        config=self.config
        config.validate()
        body={"model":config.model,"messages":messages,"tools":DEFINITIONS,
              "thinking":{"type":"disabled"},"stream":False,"max_tokens":config.max_tokens}
        request=Request(config.base_url.rstrip("/")+"/chat/completions",data=json.dumps(body,ensure_ascii=False).encode("utf-8"),
                        headers={"Content-Type":"application/json","Authorization":"Bearer "+config.api_key},method="POST")
        started=time.perf_counter()
        try:
            with build_opener(NoRedirect()).open(request,timeout=config.timeout)as response:raw=response.read(2_000_001)
            if len(raw)>2_000_000:raise APIError("工具响应超过读取上限")
            parsed=parse_tool_response(json.loads(raw.decode("utf-8")))
        except HTTPError as error:
            status=error.code;error.close()
            raise APIError(f"HTTP {status}，{HTTP_HINTS.get(status,'接口错误')}")from None
        except(TimeoutError,socket.timeout):raise APIError("工具请求超时，未自动重试")from None
        except URLError:raise APIError("工具请求网络连接失败，未自动重试")from None
        except(UnicodeError,json.JSONDecodeError):raise APIError("工具响应不是有效UTF-8 JSON")from None
        except OSError:raise APIError("工具网络读取失败，未自动重试")from None
        return redact({**parsed,"elapsed_seconds":time.perf_counter()-started,
                       "kind":"local_fixture"if config.fixture_http else"live_api"},config.api_key)
