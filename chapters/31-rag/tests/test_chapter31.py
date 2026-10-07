from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"examples"))
from retrieval import read_documents,split_text,load_index,search
from rag_answer import validate_answer,answer_from_hits
from embedding import Embedder


class Chapter31Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data,cls.vectors=load_index(ROOT/"results/index",ROOT/"data/documents")
        cls.encoder=Embedder()

    def test_exact_source_positions(self):
        for chunk in self.data["chunks"]:
            text=(ROOT/"data/documents"/chunk["source"]).read_bytes().decode("utf-8-sig")
            self.assertEqual(text[chunk["start"]:chunk["end"]],chunk["text"])
            self.assertEqual(chunk["line_start"],text.count("\n",0,chunk["start"])+1)

    def test_overlap_and_invalid_size(self):
        chunks=split_text("abcdefghij","demo",6,2)
        self.assertEqual([c["text"]for c in chunks],["abcdef","efghij"])
        with self.assertRaises(ValueError):
            split_text("demo","demo",4,4)

    def test_vectors_dimension_norm_and_repeat(self):
        vectors=self.encoder.encode(["书籍借阅期限","书籍借阅期限"])
        self.assertEqual(vectors.shape,(2,512))
        np.testing.assert_allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-6)
        np.testing.assert_array_equal(vectors[0],vectors[1])

    def test_query_instruction_and_too_long(self):
        plain=self.encoder.encode(["借书期限"])
        query=self.encoder.encode(["借书期限"],query=True)
        self.assertFalse(np.array_equal(plain,query))
        with self.assertRaises(ValueError):
            self.encoder.encode(["中"*600])

    def test_search_against_independent_cosine(self):
        query=self.encoder.encode(["书能借多久"],query=True)[0]
        hits=search(self.data,self.vectors,query,min_score=-1)
        expected=sorted([(float(np.dot(v,query)/(np.linalg.norm(v)*np.linalg.norm(query))),c["chunk_id"])for v,c in zip(self.vectors,self.data["chunks"])],reverse=True)
        self.assertEqual([h["chunk_id"]for h in hits],[item[1]for item in expected[:3]])
        self.assertAlmostEqual(hits[0]["score"],expected[0][0],places=6)

    def test_empty_index_does_not_call_model(self):
        data={"dimension":512,"chunks":[]}
        query=self.vectors[0]
        hits=search(data,np.empty((0,512),dtype=np.float32),query)
        def forbidden(_):
            raise AssertionError("不应调用模型")
        result=answer_from_hits("问题",hits,forbidden)
        self.assertEqual(result["status"],"empty")
        self.assertFalse(result["model_called"])

    def test_unknown_citation_and_fabricated_quote(self):
        hit=self.data["chunks"][0]
        for cid,quote in (("unknown","原文"),(hit["chunk_id"],"资料里没有的句子")):
            text=json.dumps({"status":"answered","answer":"回答","citations":[{"chunk_id":cid,"quote":quote}]},ensure_ascii=False)
            with self.assertRaises(ValueError):
                validate_answer(text,[hit])

    def test_conflict_requires_two_files(self):
        hit=self.data["chunks"][0]
        text=json.dumps({"status":"conflict","answer":"时间有矛盾","citations":[{"chunk_id":hit["chunk_id"],"quote":hit["text"]}]},ensure_ascii=False)
        with self.assertRaises(ValueError):
            validate_answer(text,[hit])

    def test_insufficient_and_missing_fields(self):
        result=validate_answer('{"status":"insufficient","answer":"资料未提到","citations":[]}',[])
        self.assertEqual(result["status"],"insufficient")
        with self.assertRaises(ValueError):
            validate_answer('{"answer":"回答"}',[])

    def test_quote_positions_are_exact(self):
        hit=self.data["chunks"][0]
        quote="每人每次最多借3本书"
        text=json.dumps({"status":"answered","answer":"3本","citations":[{"chunk_id":hit["chunk_id"],"quote":quote}]},ensure_ascii=False)
        citation=validate_answer(text,[hit])["citations"][0]
        source=(ROOT/"data/documents"/citation["source"]).read_text(encoding="utf-8")
        self.assertEqual(source[citation["quote_start"]:citation["quote_end"]],quote)
        self.assertEqual(citation["line_start"],11)

    def test_stale_documents_and_revision(self):
        with self.assertRaises(ValueError):
            load_index(ROOT/"results/index",revision="wrong")
        with tempfile.TemporaryDirectory()as folder:
            Path(folder,"new.md").write_text("新资料",encoding="utf-8")
            with self.assertRaises(ValueError):
                load_index(ROOT/"results/index",folder)


if __name__=="__main__":
    unittest.main()
