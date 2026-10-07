from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
from plan_core import PlanError, build_messages, empty_session, load_session, make_plan, parse_plan, save_session, validate_plan
from run_cases import TeachingReplay
from plan_assistant import ConversationRequest, Config, live_chat
from local_fixture import FIXTURE_KEY, fixture_server

CASES = json.loads((ROOT / "data/teaching-cases.json").read_text(encoding="utf-8"))
PLAN = CASES[0]["plan"]


class Chapter30Tests(unittest.TestCase):
    def test_five_inputs(self):
        for case in CASES:
            with self.subTest(question=case["input"]):
                client = TeachingReplay([json.dumps(case["plan"], ensure_ascii=False)])
                state, attempts = make_plan(empty_session(), case["input"], case["daily_minutes"], client)
                self.assertEqual(state["last_plan"], case["plan"])
                self.assertEqual(sum(task["minutes"] for task in state["last_plan"]["tasks"]), case["daily_minutes"])
                self.assertEqual(len(attempts), 1)

    def test_invalid_json_and_missing_fields(self):
        for bad in ("解释文字", '{"goal":"Python"}', '```json\n{}\n```'):
            with self.subTest(bad=bad), self.assertRaises(PlanError):
                parse_plan(bad, 20)

    def test_invalid_types_totals_and_extra_fields(self):
        variants = []
        for key, value in (("daily_minutes", True), ("daily_minutes", "20"), ("goal", " "), ("tasks", [])):
            altered = deepcopy(PLAN)
            altered[key] = value
            variants.append(altered)
        for value in (True, -1, 7):
            altered = deepcopy(PLAN)
            altered["tasks"][0]["minutes"] = value
            variants.append(altered)
        variants.append({**PLAN, "unwanted": "extra"})
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(PlanError):
                validate_plan(variant, 20)

    def test_successful_repair_only_saves_valid_pair(self):
        client = TeachingReplay(["坏JSON", json.dumps(PLAN, ensure_ascii=False)])
        state, attempts = make_plan(empty_session(), "学Python", 20, client)
        self.assertEqual(len(attempts), 2)
        self.assertFalse(attempts[0]["valid"])
        self.assertIn("校验错误", client.requests[1][-1]["content"])
        self.assertEqual([item["role"] for item in state["history"]], ["user", "assistant"])
        self.assertNotIn("坏JSON", json.dumps(state, ensure_ascii=False))

    def test_exhausted_repair_never_mutates_state(self):
        state = empty_session()
        before = deepcopy(state)
        client = TeachingReplay(["坏JSON", "坏JSON"])
        with self.assertRaisesRegex(PlanError, "2 次"):
            make_plan(state, "学Python", 20, client)
        self.assertEqual(state, before)
        self.assertEqual(len(client.requests), 2)

    def test_history_trims_whole_pairs_and_keeps_latest(self):
        history = []
        for index in range(8):
            history += [{"role": "user", "content": str(index)+"学Python"}, {"role": "assistant", "content": json.dumps(PLAN, ensure_ascii=False)}]
        messages = build_messages(history, "最新需求", 20, max_pairs=2)
        self.assertEqual([m["role"] for m in messages], ["system", "user", "assistant", "user", "assistant", "user"])
        self.assertTrue(messages[1]["content"].startswith("6"))
        self.assertEqual(messages[-1]["content"], "最新需求")
        smaller = build_messages(history, "最新需求", 20, max_pairs=3, char_budget=500)
        self.assertLessEqual(sum(len(item["content"]) for item in smaller), 500)
        self.assertEqual((len(smaller)-2) % 2, 0)

    def test_history_and_budget_invalid_before_call(self):
        client = TeachingReplay([])
        for question, minutes in ((" ", 20), ("问题", 0), ("问题", True)):
            with self.subTest(question=question, minutes=minutes), self.assertRaises(PlanError):
                make_plan(empty_session(), question, minutes, client)
        with self.assertRaises(PlanError):
            build_messages([], "长"*2000, 20)
        self.assertEqual(client.requests, [])

    def test_session_roundtrip_and_corruption_preserved(self):
        client = TeachingReplay([json.dumps(PLAN, ensure_ascii=False)])
        state, _ = make_plan(empty_session(), "学Python", 20, client)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "session.json"
            save_session(path, state)
            self.assertEqual(load_session(path), state)
            path.write_text("损坏的JSON", encoding="utf-8")
            with self.assertRaises(PlanError):
                load_session(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "损坏的JSON")

    def test_multiturn_budget_and_history(self):
        small = {"goal": "入门 Python", "daily_minutes": 10, "tasks": [{"title": "改写变量", "minutes": 10}]}
        client = TeachingReplay([json.dumps(PLAN, ensure_ascii=False), json.dumps(small, ensure_ascii=False)])
        before, _ = make_plan(empty_session(), "学Python", 20, client)
        after, _ = make_plan(before, "改为10分钟", 10, client)
        self.assertEqual(client.requests[1][1:3], before["history"])
        self.assertEqual(after["daily_minutes"], 10)
        self.assertEqual(len(after["history"]), 4)

    def test_http_adapter_sends_history_and_json_option(self):
        payload = {"id": "teaching-plan", "model": "teaching-fixture", "choices": [{"message": {"content": json.dumps(PLAN, ensure_ascii=False)}, "finish_reason": "stop"}],
                   "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}
        messages = build_messages([], "学Python", 20)
        with fixture_server(response=payload) as (base, received):
            config = Config(base_url=base, api_key=FIXTURE_KEY, fixture_http=True)
            response = live_chat(config)(messages)
            self.assertEqual(parse_plan(response["answer"], 20), PLAN)
            self.assertEqual(received[0]["body"]["messages"], messages)
            self.assertEqual(received[0]["body"]["response_format"], {"type": "json_object"})

    def test_network_errors_are_not_retried(self):
        calls = []
        def broken(messages):
            calls.append(messages)
            raise RuntimeError("网络错误")
        with self.assertRaises(RuntimeError):
            make_plan(empty_session(), "学Python", 20, broken)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
