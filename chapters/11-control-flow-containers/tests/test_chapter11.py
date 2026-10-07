import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest

CHAPTER = Path(__file__).resolve().parents[1]
# 原程序保持本章的顺序代码；测试只替换教学输入，执行相同统计主体。
BODY = (CHAPTER / "examples/study_records.py").read_text(encoding="utf-8").split("# 本章先使用", 1)[1]
BODY = "# 本章先使用" + BODY


def run_records(records):
    namespace = {"records": records}
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(BODY, "study_records.py", "exec"), namespace)
    return namespace, output.getvalue()


class RecordsTests(unittest.TestCase):
    def test_valid_and_pending(self):
        result, output = run_records([
            {"title": "变量", "done": True, "minutes": 20},
            {"title": " 循环 ", "done": False, "minutes": 15},
        ])
        self.assertEqual((result["completed"], result["pending"], result["total_minutes"]), (1, ["循环"], 35))
        self.assertIn("有效 2 条", output)

    def test_empty(self):
        result, output = run_records([])
        self.assertEqual(result["total_minutes"], 0)
        self.assertIn("未完成 []", output)

    def test_missing_field_is_invalid(self):
        result, _ = run_records([{"title": "字典", "minutes": 10}])
        self.assertEqual(result["valid_count"], 0)
        self.assertEqual(result["invalid"], ["第 1 条缺少字段"])

    def test_bad_outer_type(self):
        for data in (3, "records", {}, None):
            with self.subTest(data=data):
                _, output = run_records(data)
                self.assertEqual(output.strip(), "输入错误，请提供列表")

    def test_bad_inner_types(self):
        for data in ("record", [], 0, None):
            with self.subTest(data=data):
                result, _ = run_records([data])
                self.assertEqual(result["valid_count"], 0)

    def test_false_string_and_bool_minutes_are_rejected(self):
        for field, value in (("done", "False"), ("done", 0), ("minutes", True), ("minutes", "20"), ("minutes", -1)):
            record = {"title": "列表", "done": False, "minutes": 0}
            record[field] = value
            with self.subTest(field=field, value=value):
                result, _ = run_records([record])
                self.assertEqual(result["valid_count"], 0)

    def test_invalid_titles(self):
        for title in ("", " ", 3):
            result, _ = run_records([{"title": title, "done": True, "minutes": 1}])
            self.assertEqual(result["valid_count"], 0)

    def test_zero_minutes_is_valid(self):
        result, _ = run_records([{"title": "复习", "done": False, "minutes": 0}])
        self.assertEqual(result["valid_count"], 1)

    def test_error_and_fix_pairs(self):
        for name, error in (("missing_key", "KeyError"), ("bad_container", "TypeError"), ("bad_index", "IndexError")):
            failed = subprocess.run([sys.executable, str(CHAPTER / f"examples/errors/{name}.py")], capture_output=True, text=True, encoding="utf-8")
            fixed = subprocess.run([sys.executable, str(CHAPTER / f"examples/fixed/{name}.py")], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(failed.returncode, 1)
            self.assertIn(error, failed.stderr)
            self.assertEqual(fixed.returncode, 0)
            self.assertTrue(fixed.stdout.strip())


if __name__ == "__main__":
    unittest.main()
