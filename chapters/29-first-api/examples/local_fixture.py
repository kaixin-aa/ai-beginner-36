"""原创固定响应的本地 HTTP 服务，不运行模型、不接收真实密钥。"""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Thread
import time

FIXTURE_KEY = "local-teaching-placeholder"
FIXTURE_RESPONSE = {
    "id": "teaching-response-001", "model": "teaching-fixture",
    "choices": [{"message": {"role": "assistant", "content": "API 让你的程序向另一套服务发送请求，并取得响应。"}, "finish_reason": "stop", "index": 0}],
    "usage": {"prompt_tokens": 30, "completion_tokens": 18, "total_tokens": 48},
}


@contextmanager
def fixture_server(status=200, response=None, raw=None, delay=0):
    received = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            try:
                payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
                received.append({"path": self.path, "body": payload,
                                 "placeholder_auth": self.headers.get("Authorization") == "Bearer " + FIXTURE_KEY})
                actual_status = status
                if self.headers.get("Authorization") != "Bearer " + FIXTURE_KEY:
                    actual_status = 401
                time.sleep(delay)
                self.send_response(actual_status)
                if actual_status in (301, 302, 307, 308):
                    self.send_header("Location", "/redirected")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                content = response if response is not None else FIXTURE_RESPONSE
                body = raw if raw is not None else json.dumps(content, ensure_ascii=False).encode("utf-8")
                self.wfile.write(body)
            except ConnectionError:
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
    worker.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port), received
    finally:
        server.shutdown()
        server.server_close()
        worker.join()
