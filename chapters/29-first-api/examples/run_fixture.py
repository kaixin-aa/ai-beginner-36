"""实际执行 CLI 与本地 HTTP 往返，只生成明确标记的教学记录。"""
import json
import os
from pathlib import Path
import subprocess
import sys
from local_fixture import FIXTURE_KEY, fixture_server

ROOT = Path(__file__).resolve().parents[1]


def run():
    with fixture_server() as (base_url, received):
        # 子进程认证变量只包含占位符，绝不把真实密钥送给本地服务。
        env = dict(os.environ, AI_PROVIDER="deepseek", AI_BASE_URL=base_url,
                   AI_MODEL="teaching-fixture", AI_API_KEY_ENV="AI_FIXTURE_KEY",
                   AI_FIXTURE_KEY=FIXTURE_KEY, AI_TIMEOUT_SECONDS="2", AI_MAX_TOKENS="256",
                   PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        output = ROOT / "results/local-fixture.json"
        # 本文件为可复现教学产物。只在确认类型为本地教学记录时刷新。
        if output.exists():
            old = json.loads(output.read_text(encoding="utf-8"))
            if old.get("kind") != "local_fixture":
                raise RuntimeError("拒绝刷新类型不明的记录")
            output.unlink()
        result = subprocess.run([sys.executable, str(ROOT / "examples/qa.py"), "用一句话解释 API", "--fixture-http", "--output", str(output)],
                                capture_output=True, text=True, encoding="utf-8", env=env, timeout=10)
        assert result.returncode == 0, result.stderr
        assert len(received) == 1 and received[0]["path"] == "/chat/completions"
        assert received[0]["placeholder_auth"]
        (ROOT / "results/fixture-cli.txt").write_text(result.stdout, encoding="utf-8")
        (ROOT / "results/fixture-request.json").write_text(json.dumps(received[0]["body"], ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(result.stdout, end="")


if __name__ == "__main__":
    run()
