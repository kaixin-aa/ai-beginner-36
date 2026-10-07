import subprocess
import sys
import unittest
from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = CHAPTER_DIR / "examples"
sys.path.insert(0, str(EXAMPLES_DIR))

from study_time_calculator import calculate_study_time
from text_formatter import build_learning_card


def run_example(relative_path, user_input=""):
    return subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / relative_path)],
        input=user_input,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )


class Chapter10Tests(unittest.TestCase):
    def test_study_time_calculation(self):
        result = calculate_study_time(7, 45)
        self.assertEqual(result, (315, 5, 15, 5.25))

    def test_text_card_formatting(self):
        card, length = build_learning_card("  Python 入门  ", "  小林  ", " ai ")
        self.assertEqual(card, "[AI] Python 入门 | 作者 小林")
        self.assertEqual(length, 9)

    def test_study_time_program(self):
        result = run_example(
            "study_time_calculator.py",
            "Python 基础\n7\n45\n",
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("总时长：315 分钟", result.stdout)
        self.assertIn("换算结果：5 小时 15 分钟", result.stdout)
        self.assertIn("小数形式：5.25 小时", result.stdout)

    def test_text_formatter_program(self):
        result = run_example(
            "text_formatter.py",
            "  Python 入门  \n  小林  \n ai \n",
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[AI] Python 入门 | 作者 小林", result.stdout)
        self.assertIn("标题长度：9 个字符", result.stdout)

    def test_type_error_and_fix(self):
        broken = run_example("errors/string_number_type_error.py")
        fixed = run_example("fixed/string_number_fixed.py")
        self.assertNotEqual(broken.returncode, 0)
        self.assertIn("TypeError", broken.stderr)
        self.assertEqual(fixed.returncode, 0)
        self.assertEqual(fixed.stdout.strip(), "总分钟数 90")

    def test_conversion_error_and_fix(self):
        broken = run_example("errors/invalid_int_conversion.py")
        fixed = run_example("fixed/invalid_int_fixed.py")
        self.assertNotEqual(broken.returncode, 0)
        self.assertIn("ValueError", broken.stderr)
        self.assertEqual(fixed.returncode, 0)
        self.assertEqual(fixed.stdout.strip(), "学习分钟数 90.5")

    def test_name_error_and_fix(self):
        broken = run_example("errors/undefined_variable.py")
        fixed = run_example("fixed/undefined_variable_fixed.py")
        self.assertNotEqual(broken.returncode, 0)
        self.assertIn("NameError", broken.stderr)
        self.assertEqual(fixed.returncode, 0)
        self.assertEqual(fixed.stdout.strip(), "学习天数 7")


if __name__ == "__main__":
    unittest.main()
