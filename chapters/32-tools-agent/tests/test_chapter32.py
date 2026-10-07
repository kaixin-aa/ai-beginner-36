from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"examples"))
from agent import run_agent
from tools import calculate,dispatch,LocalSearch
from teaching_replay import Replay,tool_message,final_message
from tool_client import ToolClient,Config,parse_tool_response,APIError
sys.path.insert(0,str(ROOT.parent/"29-first-api/examples"))
from local_fixture import FIXTURE_KEY,fixture_server


class Chapter32Tests(unittest.TestCase):
    def test_arithmetic_without_eval(self):
        for expression,expected in (("14+7",21),("3*(8+9)",51),("-10/4",-2.5)):
            self.assertEqual(calculate(expression)["value"],expected)

    def test_forbidden_expressions_and_bounds(self):
        for expression in ("__import__('os').system('echo dangerous')","open('demo')","2**100","True+1","1/0","1e10","[1,2]","+"*100):
            with self.subTest(expression=expression),self.assertRaises(ValueError):calculate(expression)

    def test_tool_name_and_argument_whitelist(self):
        for name,args in (("write_file",{"path":"demo"}),("calculate",{"expression":"1+1","extra":"x"}),("search_documents",{"path":"../secret"})):
            with self.assertRaises(ValueError):dispatch(name,args,lambda _:None)

    def test_tool_result_corresponds_to_call_id(self):
        client=Replay([tool_message("calculate",{"expression":"14+7"},"calc"),final_message()])
        result=run_agent("算数",client,lambda _:None)
        self.assertEqual(result["status"],"completed")
        self.assertEqual(client.requests[1][-1]["tool_call_id"],"calc")
        self.assertEqual(json.loads(client.requests[1][-1]["content"])["data"]["value"],21)

    def test_batch_permission_check_has_no_partial_execution(self):
        response=tool_message("calculate",{"expression":"1+1"})
        bad=tool_message("write_file",{"path":"demo"},"bad")["message"]["tool_calls"][0]
        response["message"]["tool_calls"].append(bad)
        result=run_agent("执行工具",Replay([response]),lambda _:None)
        self.assertEqual((result["status"],result["tool_count"]),("blocked",0))

    def test_duplicate_and_tool_limits(self):
        client=Replay([tool_message("calculate",{"expression":"1+1"},"a"),tool_message("calculate",{"expression":"1+1"},"b")])
        result=run_agent("计算",client,lambda _:None)
        self.assertEqual(result["status"],"repeated_tool")
        self.assertEqual(result["tool_count"],1)
        result=run_agent("计算",Replay([tool_message("calculate",{"expression":"1+1"})]),lambda _:None,max_tools=0)
        self.assertEqual(result["status"],"tool_limit")

    def test_step_deadline_and_truncated_limits(self):
        result=run_agent("计算",Replay([tool_message("calculate",{"expression":"1+1"})]),lambda _:None,max_steps=1)
        self.assertEqual((result["status"],result["tool_count"]),("step_limit",0))
        ticks=iter([0,0,61,61])
        result=run_agent("计算",Replay([tool_message("calculate",{"expression":"1+1"})]),lambda _:None,clock=lambda:next(ticks))
        self.assertEqual((result["status"],result["tool_count"]),("deadline",0))
        response=tool_message("calculate",{"expression":"1+1"});response["finish_reason"]="length"
        result=run_agent("计算",Replay([response]),lambda _:None)
        self.assertEqual(result["status"],"truncated")

    def test_bad_json_and_duplicate_id(self):
        response=tool_message("calculate",{"expression":"1+1"})
        response["message"]["tool_calls"][0]["function"]["arguments"]="not-json"
        result=run_agent("计算",Replay([response]),lambda _:None)
        self.assertEqual(result["status"],"blocked")
        repeated_id=tool_message("calculate",{"expression":"1+1"},"same")
        repeated_id["message"]["tool_calls"].append(tool_message("calculate",{"expression":"2+2"},"same")["message"]["tool_calls"][0])
        result=run_agent("计算",Replay([repeated_id]),lambda _:None)
        self.assertEqual((result["status"],result["tool_count"]),("blocked",0))

    def test_real_local_search(self):
        tool=LocalSearch()
        hits=tool("借书可以借几天")["hits"]
        self.assertTrue(any("14天"in hit["text"]for hit in hits))
        with self.assertRaises(ValueError):tool("x"*201)

    def test_http_tool_protocol(self):
        call=tool_message("calculate",{"expression":"14+7"})
        data={"id":"teaching-tool","model":"teaching-fixture","choices":[{"message":call["message"],"finish_reason":"tool_calls"}],"usage":call["usage"]}
        with fixture_server(response=data)as(base,received):
            client=ToolClient(Config(base_url=base,api_key=FIXTURE_KEY,fixture_http=True))
            result=client([{"role":"user","content":"14+7"}])
            self.assertEqual(result["finish_reason"],"tool_calls")
            self.assertEqual(received[0]["body"]["thinking"],{"type":"disabled"})
            self.assertEqual(len(received[0]["body"]["tools"]),2)

    def test_malformed_response_rejected(self):
        with self.assertRaises(APIError):parse_tool_response({"choices":[]})


if __name__=="__main__":unittest.main()
