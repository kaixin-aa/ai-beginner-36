"""离线核对已保存的真实工具轨迹，不再调用 API。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def audit():
    records=[]
    for file in sorted((ROOT/"results").glob("live-agent-*.json")):
        data=json.loads(file.read_text(encoding="utf-8"))
        models=[x for x in data["trace"]if x["event"]=="model_response"]
        tools=[x for x in data["trace"]if x["event"]=="tool_result"]
        assert all(x["response"]["kind"]=="live_api"for x in models)
        assert data["model_requests"]==len(models)and data["tool_count"]==len(tools)<=4
        assert data["total_tokens"]==sum(x["response"]["usage"]["total_tokens"]for x in models)
        proposed={c["id"]:c["function"]["name"]for x in models for c in x["response"]["message"].get("tool_calls",[])}
        assert all(proposed[x["tool_call_id"]]==x["name"]for x in tools)
        records.append({"file":file.name,"status":data["status"],"requests":len(models),"tokens":data["total_tokens"],"tools":[x["name"]for x in tools]})
        if data["status"]=="completed"and len(tools)==2:
            assert [x["name"]for x in tools]==["search_documents","calculate"]
            assert tools[0]["step"]<tools[1]["step"]
            assert tools[1]["result"]["data"]["value"]==21
            assert any("14天"in h["text"]and "7天"in h["text"]for h in tools[0]["result"]["data"]["hits"])
            assert "21"in data["answer"]and "guide.md"in data["answer"]
    assert len(records)==3
    assert sum(x["status"]=="completed"for x in records)==2
    assert any(x["status"]=="tool_limit"for x in records)
    result={"kind":"offline_audit","records":records,"requests":sum(x["requests"]for x in records),"total_tokens":sum(x["tokens"]for x in records),"accepted":True,
            "manual_source_check":"两数均在guide.md第11行。最终回答行号为片段范围，引用精度见验收说明。"}
    (ROOT/"results/live-audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("真实调用离线核对",result["requests"],result["total_tokens"])

if __name__=="__main__":audit()
