"""验证真实 HTTP 传输、错误分支和秘密不进入记录。"""
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from api_client import APIError, Config, ask, parse_response
from local_fixture import FIXTURE_KEY, FIXTURE_RESPONSE, fixture_server


def config_at(base):
    return Config(base_url=base, model="teaching-fixture", api_key=FIXTURE_KEY, fixture_http=True, timeout=2)


class Chapter29Tests(unittest.TestCase):
    def test_utf8_http_roundtrip(self):
        with fixture_server() as (base, received):
            result = ask(config_at(base), "解释 API")
            self.assertEqual(result["answer"], FIXTURE_RESPONSE["choices"][0]["message"]["content"])
            self.assertEqual(result["kind"], "local_fixture")
            self.assertEqual(result["usage"]["total_tokens"], 48)
            self.assertEqual(received[0]["path"], "/chat/completions")
            self.assertEqual(received[0]["body"]["messages"][1]["content"], "解释 API")
            self.assertEqual(received[0]["body"]["thinking"], {"type": "disabled"})
            self.assertTrue(received[0]["placeholder_auth"])

    def test_missing_key_and_empty_question_never_send(self):
        with fixture_server() as (base, received):
            for config, prompt in ((replace(config_at(base), api_key=""), "问题"), (config_at(base), "  ")):
                with self.assertRaises(APIError):
                    ask(config, prompt)
            self.assertEqual(received, [])

    def test_url_boundaries(self):
        for base, fixture in (("http://example.com", False), ("https://user:pass@example.com", False),
                              ("https://example.com?key=secret", False), ("https://example.com", True)):
            with self.subTest(base=base), self.assertRaises(APIError):
                Config(base_url=base, api_key=FIXTURE_KEY, fixture_http=fixture).validate()

    def test_invalid_configuration(self):
        for field, value in (("AI_TIMEOUT_SECONDS", "nan"), ("AI_TIMEOUT_SECONDS", "0"),
                             ("AI_MAX_TOKENS", "-1"), ("AI_MAX_TOKENS", "oops"), ("AI_MODEL", "")):
            with self.subTest(field=field, value=value), patch.dict(os.environ, {"DEEPSEEK_API_KEY": FIXTURE_KEY, field: value}, clear=True):
                with self.assertRaises(APIError):
                    Config.from_env()

    def test_http_status_hints_without_raw_error(self):
        for status in (400, 401, 402, 422, 429, 500, 503):
            with self.subTest(status=status), fixture_server(status=status, raw=b"secret-error-body") as (base, received):
                with self.assertRaises(APIError) as caught:
                    ask(config_at(base), "问题")
                self.assertIn(str(status), str(caught.exception))
                self.assertNotIn("secret-error-body", str(caught.exception))
                self.assertEqual(len(received), 1)  # 无自动重试。

    def test_socket_timeout(self):
        with fixture_server(delay=0.15) as (base, received):
            with self.assertRaisesRegex(APIError, "超时"):
                ask(replace(config_at(base), timeout=0.02), "问题")
            self.assertEqual(len(received), 1)

    def test_invalid_json_and_usage(self):
        with fixture_server(raw=b"not-json") as (base, _):
            with self.assertRaisesRegex(APIError, "JSON"):
                ask(config_at(base), "问题")
        for bad in ({}, {**FIXTURE_RESPONSE, "choices": []}, {**FIXTURE_RESPONSE, "usage": {"prompt_tokens": 30, "completion_tokens": 18, "total_tokens": 99}}):
            with self.subTest(bad=bad), self.assertRaises(APIError):
                parse_response(bad)

    def test_truncation_is_not_complete(self):
        data = deepcopy(FIXTURE_RESPONSE)
        data["choices"][0]["finish_reason"] = "length"
        result = parse_response(data)
        self.assertFalse(result["complete"])
        self.assertEqual(result["finish_reason"], "length")

    def test_redirect_is_not_followed(self):
        with fixture_server(status=307) as (base, received):
            with self.assertRaisesRegex(APIError, "307"):
                ask(config_at(base), "问题")
            self.assertEqual(len(received), 1)

    def test_secret_repr_and_response_redaction(self):
        data = deepcopy(FIXTURE_RESPONSE)
        data["choices"][0]["message"]["content"] = "回显 " + FIXTURE_KEY
        data["id"] = FIXTURE_KEY
        with fixture_server(response=data) as (base, _):
            config = config_at(base)
            self.assertNotIn(FIXTURE_KEY, repr(config))
            result = ask(config, "问题")
            self.assertNotIn(FIXTURE_KEY, json.dumps(result))
            self.assertIn("[已隐藏]", result["answer"])

    def test_cli_records_and_preserves_existing_file(self):
        script = Path(__file__).resolve().parents[1] / "examples/qa.py"
        with tempfile.TemporaryDirectory() as folder, fixture_server() as (base, received):
            output = Path(folder) / "record.json"
            env = dict(os.environ, AI_PROVIDER="deepseek", AI_BASE_URL=base, AI_MODEL="teaching-fixture",
                       AI_API_KEY_ENV="AI_FIXTURE_KEY", AI_FIXTURE_KEY=FIXTURE_KEY,
                       AI_TIMEOUT_SECONDS="2", AI_MAX_TOKENS="256", PYTHONUTF8="1")
            args = [sys.executable, str(script), "一句话解释 API", "--fixture-http", "--output", str(output)]
            first = subprocess.run(args, env=env, capture_output=True, text=True, encoding="utf-8", timeout=10)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            self.assertEqual(json.loads(original)["kind"], "local_fixture")
            self.assertNotIn(FIXTURE_KEY, original.decode("utf-8"))
            second = subprocess.run(args, env=env, capture_output=True, text=True, encoding="utf-8", timeout=10)
            self.assertEqual(second.returncode, 1)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(len(received), 1)


if __name__ == "__main__":
    unittest.main()
