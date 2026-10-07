import json
from pathlib import Path
import time
import numpy as np
from embedding import Embedder
from retrieval import build_index,load_index,search
ROOT=Path(__file__).resolve().parents[1]


def run():
    encoder=Embedder()
    started=time.perf_counter()
    data,vectors=build_index(ROOT/"data/documents",ROOT/"results/index",encoder)
    loaded,restored=load_index(ROOT/"results/index",ROOT/"data/documents",encoder.revision)
    assert loaded==data and np.array_equal(restored,vectors)
    cases=json.loads((ROOT/"data/questions.json").read_text(encoding="utf-8"))
    queries=encoder.encode([case["question"] for case in cases],query=True)
    records=[{**case,"hits":search(data,vectors,query),"all_scores":(vectors@query).tolist()}for case,query in zip(cases,queries)]
    result={"model":encoder.metadata,"dimension":encoder.dimension,"chunk_count":len(data["chunks"]),
            "parameter_count":sum(p.numel()for p in encoder.model.parameters()),"threshold":0.55,"top_k":3,
            "records":records,"vectors_reload_equal":True,"elapsed_seconds":time.perf_counter()-started}
    (ROOT/"results/retrieval-results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for record in records:
        print(record["split"],record["question"],[(h["source"],round(h["score"],4))for h in record["hits"]])
    print("块数",len(data["chunks"]),"向量形状",vectors.shape,"重载一致",True)


if __name__=="__main__":
    run()
