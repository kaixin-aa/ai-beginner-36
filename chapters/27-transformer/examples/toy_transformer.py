"""单层、两头、前置LayerNorm的字符级教学语言模型。"""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import torch
from torch import nn
from torch.nn import functional as F

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {"width":16,"heads":2,"ff_width":32,"max_context":16,"norm_eps":1e-5}


class CharacterTokenizer:
    def __init__(self,tokens):
        if tokens[:3] != ["<PAD>","<BOS>","<EOS>"] or len(tokens)!=len(set(tokens)):
            raise ValueError("词表须含固定特殊Token且不重复")
        self.tokens = list(tokens)
        self.ids = {token:i for i,token in enumerate(tokens)}
        self.pad,self.bos,self.eos = 0,1,2

    @classmethod
    def from_sentences(cls,sentences):
        return cls(["<PAD>","<BOS>","<EOS>"]+sorted(set("".join(sentences))))

    def encode(self,text,bos=False,eos=False):
        if not isinstance(text,str):
            raise ValueError("输入必须为字符串")
        if any(char not in self.ids for char in text):
            raise ValueError("出现词表未覆盖的字符")
        return ([self.bos] if bos else [])+[self.ids[char] for char in text]+([self.eos] if eos else [])

    def decode(self,ids):
        if any(not isinstance(i,int) or i<0 or i>=len(self.tokens) for i in ids):
            raise ValueError("编号越界")
        return "".join(self.tokens[i] for i in ids if i>=3)


class TinyTransformer(nn.Module):
    def __init__(self,vocab_size,**config):
        super().__init__()
        self.config = dict(config)
        width,heads = config["width"],config["heads"]
        if width%heads:
            raise ValueError("特征维度必须能被头数整除")
        self.vocab_size,self.width,self.heads = vocab_size,width,heads
        self.token_embedding = nn.Embedding(vocab_size,width)
        self.position_embedding = nn.Embedding(config["max_context"],width)
        self.norm1 = nn.LayerNorm(width,eps=config["norm_eps"])
        self.qkv = nn.Linear(width,3*width)
        self.attention_out = nn.Linear(width,width)
        self.norm2 = nn.LayerNorm(width,eps=config["norm_eps"])
        self.feed_forward = nn.Sequential(nn.Linear(width,config["ff_width"]),nn.ReLU(),nn.Linear(config["ff_width"],width))
        self.final_norm = nn.LayerNorm(width,eps=config["norm_eps"])
        self.language_head = nn.Linear(width,vocab_size)

    def forward(self,ids,trace=False):
        if ids.ndim != 2 or ids.dtype != torch.long or ids.shape[1]<1 or ids.shape[1]>self.config["max_context"]:
            raise ValueError("输入须为非空B×T Long编号，长度不能超过上下文上限")
        if (ids<0).any() or (ids>=self.vocab_size).any():
            raise ValueError("Token编号越界")
        b,t = ids.shape
        shapes = {"ids":list(ids.shape)}
        token = self.token_embedding(ids)
        position = self.position_embedding(torch.arange(t,device=ids.device))[None,:,:]
        x = token+position
        shapes.update({"token_embedding":list(token.shape),"position_embedding":list(position.shape),"embedding_sum":list(x.shape)})
        normalized = self.norm1(x)
        qkv = self.qkv(normalized).reshape(b,t,3,self.heads,self.width//self.heads).permute(2,0,3,1,4)
        q,k,v = qkv.unbind(0)
        attended = F.scaled_dot_product_attention(q,k,v,dropout_p=0.0,is_causal=True)
        joined = attended.transpose(1,2).contiguous().reshape(b,t,self.width)
        branch = self.attention_out(joined)
        x = x+branch
        shapes.update({"norm1":list(normalized.shape),"qkv_each":list(q.shape),"head_output":list(attended.shape),"concat":list(joined.shape),"attention_projection":list(branch.shape),"residual1":list(x.shape)})
        normalized = self.norm2(x)
        hidden = self.feed_forward[1](self.feed_forward[0](normalized))
        branch = self.feed_forward[2](hidden)
        x = x+branch
        logits = self.language_head(self.final_norm(x))
        shapes.update({"norm2":list(normalized.shape),"ff_hidden":list(hidden.shape),"ff_output":list(branch.shape),"residual2":list(x.shape),"final_norm":list(x.shape),"logits":list(logits.shape)})
        return (logits,shapes) if trace else logits


def load_corpus():
    return json.loads((ROOT/"data/teaching-corpus.json").read_text(encoding="utf-8"))


def make_batch(sentences,tokenizer):
    sequences = [tokenizer.encode(text,bos=True,eos=True) for text in sentences]
    length = max(len(row)-1 for row in sequences)
    x = torch.full((len(sequences),length),tokenizer.pad,dtype=torch.long)
    y = torch.full((len(sequences),length),-100,dtype=torch.long)
    for index,row in enumerate(sequences):
        x[index,:len(row)-1] = torch.tensor(row[:-1])
        y[index,:len(row)-1] = torch.tensor(row[1:])
    return x,y


def language_loss(model,x,y):
    logits = model(x)
    return F.cross_entropy(logits.reshape(-1,model.vocab_size),y.reshape(-1),ignore_index=-100)


def train_model(steps=300):
    if not isinstance(steps,int) or isinstance(steps,bool) or steps<1:
        raise ValueError("步数须为正整数")
    torch.manual_seed(42)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    data = load_corpus()
    tokenizer = CharacterTokenizer.from_sentences(data["sentences"])
    x,y = make_batch(data["sentences"],tokenizer)
    started = perf_counter()
    model = TinyTransformer(len(tokenizer.tokens),**CONFIG)
    optimizer = torch.optim.Adam(model.parameters(),lr=0.01)
    initial = float(language_loss(model,x,y).detach())
    history = [{"step":0,"train_loss":initial}]
    for step in range(1,steps+1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = language_loss(model,x,y)
        loss.backward()
        optimizer.step()
        if step%10==0 or step==steps:
            model.eval()
            with torch.no_grad():
                history.append({"step":step,"train_loss":float(language_loss(model,x,y))})
    model.eval()
    summary = {"torch":str(torch.__version__),"device":"cpu","threads":1,"seed":42,"steps":steps,"optimizer":"Adam","learning_rate":0.01,"rows":len(data["sentences"]),"vocab_size":len(tokenizer.tokens),"parameters":sum(p.numel() for p in model.parameters()),"nonpadding_targets":int((y!=-100).sum()),"batch_shape":list(x.shape),"initial_train_loss":initial,"final_train_loss":history[-1]["train_loss"],"seconds":perf_counter()-started,"independent_test":False,"config":CONFIG,"corpus_sha256":hashlib.sha256((ROOT/"data/teaching-corpus.json").read_bytes()).hexdigest()}
    return model,tokenizer,history,summary


def save_model(model,tokenizer,path):
    torch.save({"state_dict":model.state_dict(),"tokens":tokenizer.tokens,"config":model.config,"architecture":"one-block-pre-ln-causal-character-v1","torch":str(torch.__version__)},path)


def load_model(path):
    payload = torch.load(path,map_location="cpu",weights_only=True)
    if payload["architecture"]!="one-block-pre-ln-causal-character-v1" or payload["torch"]!=str(torch.__version__):
        raise ValueError("模型结构或版本不符")
    tokenizer = CharacterTokenizer(payload["tokens"])
    model = TinyTransformer(len(tokenizer.tokens),**payload["config"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model,tokenizer


def generate(model,tokenizer,prompt,max_new_tokens=12,temperature=1.0,seed=42,greedy=True,top_k=None):
    if not isinstance(max_new_tokens,int) or isinstance(max_new_tokens,bool) or max_new_tokens<1:
        raise ValueError("新Token上限须为正整数")
    if not 0<temperature<float("inf"):
        raise ValueError("温度须为有限正数")
    if top_k is not None and (not isinstance(top_k,int) or isinstance(top_k,bool) or not 1<=top_k<=len(tokenizer.tokens)-2):
        raise ValueError("top_k范围不正确")
    ids = tokenizer.encode(prompt,bos=True)
    if len(ids)>model.config["max_context"]:
        raise ValueError("提示超过上下文上限")
    model.eval()
    generator = torch.Generator().manual_seed(seed)
    trace,reason = [],"max_new_tokens"
    for step in range(1,max_new_tokens+1):
        if len(ids)>=model.config["max_context"]:
            reason = "context_limit"
            break
        with torch.no_grad():
            logits = model(torch.tensor([ids],dtype=torch.long))[0,-1].clone()
            logits[tokenizer.pad] = logits[tokenizer.bos] = -torch.inf
            logits = logits/temperature
            if top_k is not None:
                selected = logits.topk(top_k).indices
                mask = torch.full_like(logits,-torch.inf)
                mask[selected] = logits[selected]
                logits = mask
            probabilities = torch.softmax(logits,dim=-1)
            next_id = int(probabilities.argmax()) if greedy else int(torch.multinomial(probabilities,1,generator=generator))
        ranks = probabilities.topk(3)
        trace.append({"step":step,"prefix_before":tokenizer.decode(ids),"input_tokens":len(ids),"selected_id":next_id,"selected_token":tokenizer.tokens[next_id],"selected_probability":float(probabilities[next_id]),"top3":[{"token":tokenizer.tokens[int(i)],"probability":float(p)} for p,i in zip(ranks.values,ranks.indices)]})
        ids.append(next_id)
        if next_id==tokenizer.eos:
            reason = "eos"
            break
    return {"prompt":prompt,"text":tokenizer.decode(ids),"stop_reason":reason,"trace":trace,"temperature":temperature,"greedy":greedy,"seed":seed,"top_k":top_k}
