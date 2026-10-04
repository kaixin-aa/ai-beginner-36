"""单次 Chat Completions 请求，配置与提供方差异集中在此文件。"""
from dataclasses import dataclass, field
import json
import math
import os
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class APIError(Exception):
    """只给出固定诊断，不输出请求头、密钥或服务端原始错误体。"""


HTTP_HINTS = {
    400: "请求格式错误，请核对 JSON 与接口路径",
    401: "认证失败，请在本机检查 API Key",
    402: "余额不足，请检查开发平台余额",
    403: "没有访问权限，请检查账号与模型权限",
    404: "接口或模型未找到，请核对地址和模型名",
    422: "参数无效，请检查模型与参数范围",
    429: "请求过快，请稍后手动重试",
    500: "服务端故障，请稍后手动重试",
    503: "服务繁忙，请稍后手动重试",
}


@dataclass(frozen=True)
class Config:
    provider: str = "deepseek"
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-flash"
    api_key_env: str = "DEEPSEEK_API_KEY"
    timeout: float = 30.0
    max_tokens: int = 256
    fixture_http: bool = False
    api_key: str = field(default="", repr=False)

    @classmethod
    def from_env(cls, fixture_http=False):
        key_name = os.getenv("AI_API_KEY_ENV", "DEEPSEEK_API_KEY")
        try:
            config = cls(
                provider=os.getenv("AI_PROVIDER", "deepseek"),
                base_url=os.getenv("AI_BASE_URL", "https://api.deepseek.com").rstrip("/"),
                model=os.getenv("AI_MODEL", "deepseek-flash"),
                api_key_env=key_name,
                timeout=float(os.getenv("AI_TIMEOUT_SECONDS", "30")),
                max_tokens=int(os.getenv("AI_MAX_TOKENS", "256")),
                api_key=os.getenv(key_name, "").strip(),
                fixture_http=fixture_http,
            )
        except (ValueError, OverflowError):
            raise APIError("超时秒数和输出上限必须是有效数字") from None
        config.validate()
        return config

    def validate(self):
        try:
            url = urlsplit(self.base_url)
            url.port
        except ValueError:
            raise APIError("接口地址或端口格式无效") from None
        local_fixture = self.fixture_http and url.hostname in ("127.0.0.1", "localhost", "::1")
        if not url.hostname or url.username or url.password or url.query or url.fragment:
            raise APIError("接口地址必须包含主机，不能包含登录信息、查询串或片段")
        if url.scheme != "https" and not (url.scheme == "http" and local_fixture):
            raise APIError("真实服务必须使用 HTTPS，本地教学服务除外")
        if self.fixture_http and not local_fixture:
            raise APIError("教学模式仅允许回环地址")
        if not self.model.strip() or not self.provider.strip():
            raise APIError("模型名和提供方不能为空")
        if not self.api_key or self.api_key in ("YOUR_API_KEY", "replace_me"):
            raise APIError(f"未配置 {self.api_key_env}，请在本机设置环境变量")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise APIError("超时秒数必须是有限正数")
        if type(self.max_tokens) is not int or self.max_tokens <= 0:
            raise APIError("输出上限必须是正整数")
        if "\r" in self.api_key or "\n" in self.api_key:
            raise APIError("密钥不能包含换行")

    def payload(self, question):
        self.validate()
        if not isinstance(question, str) or not question.strip():
            raise APIError("问题不能为空")
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是中文入门教程助手。请简短、具体地回答。"},
                {"role": "user", "content": question.strip()},
            ],
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        if self.provider == "deepseek":
            body["thinking"] = {"type": "disabled"}
        return body


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # 防止带认证头的请求被重定向到别处。
        return None


def parse_response(data):
    try:
        choice = data["choices"][0]
        text = choice["message"]["content"]
        finish = choice["finish_reason"]
        usage = {name: data["usage"][name] for name in ("prompt_tokens", "completion_tokens", "total_tokens")}
        response_id, model = data["id"], data["model"]
        valid = (
            isinstance(text, str) and bool(text.strip())
            and finish in ("stop", "length")
            and isinstance(response_id, str) and bool(response_id)
            and isinstance(model, str) and bool(model)
            and all(type(value) is int and value >= 0 for value in usage.values())
            and usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]
        )
        if not valid:
            raise ValueError()
    except (KeyError, IndexError, TypeError, ValueError):
        raise APIError("响应缺少有效文本、结束原因或用量，请核对提供方的响应格式") from None
    return {"response_id": response_id, "returned_model": model, "answer": text,
            "finish_reason": finish, "usage": usage, "complete": finish == "stop"}


def ask(config, question):
    payload = config.payload(question)
    request = Request(
        config.base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + config.api_key},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with build_opener(NoRedirect()).open(request, timeout=config.timeout) as response:
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise APIError("响应超过本教程的 2 MB 读取上限")
        parsed = parse_response(json.loads(raw.decode("utf-8")))
    except HTTPError as error:
        status = error.code
        error.close()
        hint = HTTP_HINTS.get(status, "接口返回错误，请检查配置，程序未自动重试")
        raise APIError(f"HTTP {status}，{hint}") from None
    except (TimeoutError, socket.timeout):
        raise APIError("请求超时，结果未知，请稍后检查再决定是否重试") from None
    except URLError as error:
        if isinstance(error.reason, (TimeoutError, socket.timeout)):
            raise APIError("请求超时，结果未知，请稍后检查再决定是否重试") from None
        raise APIError("网络连接失败，请检查网络、接口地址与证书") from None
    except (UnicodeError, json.JSONDecodeError):
        raise APIError("响应无法解析为 UTF-8 JSON") from None
    except OSError:
        raise APIError("网络读取失败，结果未知，请检查连接") from None
    result = {
        "kind": "local_fixture" if config.fixture_http else "live_api",
        "provider": config.provider, "base_url": config.base_url,
        "requested_model": config.model, "question": question.strip(),
        **parsed, "elapsed_seconds": round(time.perf_counter() - started, 4),
    }
    # 即使服务端在文本或 ID 中回显密钥，也不把它写入屏幕与结果。
    return redact(result, config.api_key)


def redact(value, secret):
    if isinstance(value, str):
        return value.replace(secret, "[已隐藏]") if secret else value
    if isinstance(value, dict):
        return {key: redact(item, secret) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item, secret) for item in value]
    return value
