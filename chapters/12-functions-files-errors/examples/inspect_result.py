"""读回 JSON，核对字段及首项。"""
import json
from pathlib import Path

result_file = Path(__file__).resolve().parents[1] / "results/word_counts.json"
with result_file.open("r", encoding="utf-8") as file:
    result = json.load(file)
print("总词数", result["total_words"])
print("不同词数", result["unique_words"])
if result["frequencies"]:
    print("最高频词", result["frequencies"][0])
else:
    print("没有词频条目")
