import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHAPTER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHAPTER / "examples"))
from text_stats import count_words, tokenize


class WordCounterTests(unittest.TestCase):
    def run_cli(self, input_file, output_file):
        return subprocess.run([sys.executable, str(CHAPTER / "examples/word_counter.py"), str(input_file), str(output_file)], capture_output=True, text=True, encoding="utf-8")

    def test_normal_and_json_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "out.json"
            run = self.run_cli(CHAPTER / "data/sample.txt", target)
            self.assertEqual(run.returncode, 0, run.stderr)
            expected = json.loads((CHAPTER / "data/expected.json").read_text(encoding="utf-8"))
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), expected)

    def test_empty_and_whitespace(self):
        for text in ("", " \n\t"):
            self.assertEqual(count_words(text), {"total_words": 0, "unique_words": 0, "frequencies": []})
        with tempfile.TemporaryDirectory() as directory:
            run = self.run_cli(CHAPTER / "data/empty.txt", Path(directory) / "empty.json")
            self.assertEqual(run.returncode, 0)
            self.assertIn("文本为空", run.stdout)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "out.json"
            run = self.run_cli(Path(directory) / "missing.txt", target)
            self.assertEqual(run.returncode, 2)
            self.assertIn("找不到输入文件", run.stdout)
            self.assertFalse(target.exists())

    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.txt"
            source.write_bytes(b"\xff\xfe")
            target = Path(directory) / "out.json"
            run = self.run_cli(source, target)
            self.assertEqual(run.returncode, 2)
            self.assertIn("不是有效的 UTF-8", run.stdout)
            self.assertFalse(target.exists())

    def test_same_path_preserves_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.txt"
            source.write_text("AI", encoding="utf-8")
            run = self.run_cli(source, source)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(source.read_text(encoding="utf-8"), "AI")

    def test_missing_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            run = self.run_cli(CHAPTER / "data/sample.txt", Path(directory) / "missing/out.json")
            self.assertEqual(run.returncode, 2)
            self.assertIn("无法保存结果", run.stdout)

    def test_rule_and_stable_ties(self):
        self.assertEqual(tokenize("AI ai don't 中文 123"), ["ai", "ai", "don't"])
        self.assertEqual(count_words("B a")['frequencies'], [{"word": "a", "count": 1}, {"word": "b", "count": 1}])

    def test_chinese_only(self):
        self.assertEqual(count_words("学习人工智能")['total_words'], 0)

    def test_error_fix_pairs(self):
        for name, error in (("missing_file", "FileNotFoundError"), ("bad_encoding", "UnicodeDecodeError")):
            failed = subprocess.run([sys.executable, str(CHAPTER / f"examples/errors/{name}.py")], capture_output=True, text=True, encoding="utf-8")
            fixed = subprocess.run([sys.executable, str(CHAPTER / f"examples/fixed/{name}.py")], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(failed.returncode, 1)
            self.assertIn(error, failed.stderr)
            self.assertEqual(fixed.returncode, 0)


if __name__ == "__main__":
    unittest.main()
