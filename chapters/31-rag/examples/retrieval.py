"""只读取指定资料目录，保存精确字符位置和行号的 NumPy 向量索引。"""
import hashlib
import json
from pathlib import Path
import numpy as np


def split_text(text, source, max_chars=140, overlap=30):
    if type(max_chars) is not int or type(overlap) is not int or not 0 <= overlap < max_chars:
        raise ValueError("重叠必须小于正整数块长度")
    chunks = []
    for begin in range(0,len(text),max_chars-overlap):
        end = min(begin+max_chars,len(text))
        raw = text[begin:end]
        left = len(raw)-len(raw.lstrip())
        right = len(raw.rstrip())
        if left >= right:
            continue
        start, stop = begin+left, begin+right
        chunks.append({"chunk_id": f"{source}@{start}-{stop}", "source": source,
                       "start": start, "end": stop, "line_start": text.count("\n",0,start)+1,
                       "line_end": text.count("\n",0,stop-1)+1, "text": text[start:stop]})
        if end == len(text):
            break
    return chunks


def read_documents(folder):
    folder = Path(folder).resolve()
    chunks, manifest = [], []
    for file in sorted(folder.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in (".md",".txt"):
            continue
        if not file.resolve().is_relative_to(folder):
            raise ValueError("资料路径超出指定目录")
        raw = file.read_bytes()
        if len(raw)>100_000:
            raise ValueError("教学版本每份资料最多100 KB")
        text = raw.decode("utf-8-sig")
        source = file.relative_to(folder).as_posix()
        manifest.append({"source": source, "sha256": hashlib.sha256(raw).hexdigest()})
        chunks += split_text(text,source)
    return chunks, manifest


def build_index(folder, output, embedder):
    chunks, manifest = read_documents(folder)
    vectors = embedder.encode([chunk["text"] for chunk in chunks])
    output = Path(output)
    output.mkdir(parents=True,exist_ok=True)
    data = {"version":1,"model_revision":embedder.revision,"dimension":embedder.dimension,
            "documents":manifest,"chunks":chunks,"chunk_chars":140,"overlap_chars":30}
    (output/"index.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    np.save(output/"vectors.npy",vectors,allow_pickle=False)
    return data,vectors


def load_index(output, folder=None, revision=None):
    output = Path(output)
    data = json.loads((output/"index.json").read_text(encoding="utf-8"))
    vectors = np.load(output/"vectors.npy",allow_pickle=False)
    if vectors.shape != (len(data["chunks"]),data["dimension"]) or not np.isfinite(vectors).all():
        raise ValueError("索引行数、维度或数值无效")
    if len(vectors) and not np.allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-5):
        raise ValueError("索引向量必须为单位长度")
    if revision is not None and revision != data["model_revision"]:
        raise ValueError("问题向量与索引模型版本不一致，请重新建立索引")
    if folder is not None:
        _, manifest = read_documents(folder)
        if manifest != data["documents"]:
            raise ValueError("资料已改变，请重新建立索引")
    return data,vectors


def search(data,vectors,query_vector,top_k=3,min_score=0.55):
    if type(top_k) is not int or top_k <= 0 or not np.isfinite(min_score) or not -1 <= min_score <= 1:
        raise ValueError("检索数量和相似度门槛无效")
    query_vector = np.asarray(query_vector,dtype=np.float32)
    if query_vector.shape != (data["dimension"],) or not np.isfinite(query_vector).all() or not np.isclose(np.linalg.norm(query_vector),1,atol=1e-5):
        raise ValueError("问题必须是与索引同维度的单位向量")
    scores = vectors @ query_vector
    order = np.argsort(-scores,kind="stable")[:top_k]
    return [{**data["chunks"][i],"score":float(scores[i])} for i in order if scores[i]>=min_score]
