"""固定公开权重、CPU、CLS pooling 和单位长度中文向量。"""
import json
from pathlib import Path
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

PROJECT = Path(__file__).resolve().parents[3]
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："


class Embedder:
    dimension = 512

    def __init__(self, metadata_path=None):
        metadata_path = Path(metadata_path) if metadata_path else PROJECT / "review/rag-model-metadata.json"
        self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        snapshot = PROJECT / self.metadata["snapshot"].replace("\\","/")
        if not (snapshot/"model.safetensors").exists():
            raise FileNotFoundError("模型缓存缺失，请先运行 review/prepare_rag_model.py")
        self.tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
        self.model = AutoModel.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False, use_safetensors=True).to("cpu").eval()
        torch.set_num_threads(1)
        self.revision = self.metadata["revision"]
        assert self.model.config.hidden_size == self.dimension

    def encode(self, texts, query=False):
        if not texts:
            return np.empty((0,self.dimension),dtype=np.float32)
        if any(not isinstance(text,str) or not text.strip() for text in texts):
            raise ValueError("向量输入必须是非空文本")
        texts = [QUERY_INSTRUCTION+text if query else text for text in texts]
        token_lists = self.tokenizer(texts, add_special_tokens=True, truncation=False)["input_ids"]
        if any(len(tokens)>512 for tokens in token_lists):
            raise ValueError("文本超过512 Token，请缩短切分块或问题")
        vectors = []
        with torch.inference_mode():
            for start in range(0,len(texts),8):
                encoded = self.tokenizer(texts[start:start+8],padding=True,truncation=False,return_tensors="pt")
                hidden = self.model(**encoded).last_hidden_state[:,0]
                vectors.append(torch.nn.functional.normalize(hidden,p=2,dim=1).numpy())
        return np.concatenate(vectors).astype(np.float32)
