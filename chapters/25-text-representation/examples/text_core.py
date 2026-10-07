"""字符计数、限定词表最长匹配、查表向量与简化字符BPE。"""
from collections import Counter
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_data():
    return json.loads((ROOT/"data/teaching-texts.json").read_text(encoding="utf-8"))


def tokenize_words(text, vocabulary):
    if not isinstance(text,str) or not text.strip():
        raise ValueError("文本不能为空")
    ordered = sorted(vocabulary,key=lambda token:(-len(token),token))
    result,position = [],0
    while position < len(text):
        if text[position].isspace() or text[position] in "，。！？,.!?":
            position += 1
            continue
        token = next((token for token in ordered if text.startswith(token,position)),None)
        if token is None:
            raise ValueError(f"词表未覆盖位置{position}的文字，需明确补充词或更换输入")
        result.append(token)
        position += len(token)
    if not result:
        raise ValueError("没有可用Token")
    return result


def vocabulary_and_matrix(vectors):
    tokens = sorted(vectors)
    ids = {token:index for index,token in enumerate(tokens)}
    matrix = np.array([vectors[token] for token in tokens],dtype=np.float64)
    if matrix.ndim != 2 or not np.isfinite(matrix).all():
        raise ValueError("向量表必须是有限二维矩阵")
    return ids,matrix


def sentence_vector(text,vectors):
    ids,matrix = vocabulary_and_matrix(vectors)
    tokens = tokenize_words(text,ids)
    numbers = [ids[token] for token in tokens]
    return matrix[numbers].mean(axis=0),tokens,numbers


def cosine(left,right):
    left,right = np.asarray(left,dtype=float),np.asarray(right,dtype=float)
    if left.ndim != 1 or left.shape != right.shape or not np.isfinite(left).all() or not np.isfinite(right).all():
        raise ValueError("两向量须为同形状的有限一维数组")
    denominator = np.linalg.norm(left)*np.linalg.norm(right)
    if denominator == 0:
        raise ValueError("零向量没有方向，不能计算余弦相似度")
    return float(np.clip(np.dot(left,right)/denominator,-1,1))


def character_vectors(sentences):
    characters = sorted(set("".join(sentences)))
    counts = [Counter(sentence) for sentence in sentences]
    return characters,np.array([[count[char] for char in characters] for count in counts],dtype=float)


def merge_pair(parts,pair):
    result,index = [],0
    while index < len(parts):
        if index+1 < len(parts) and (parts[index],parts[index+1]) == tuple(pair):
            result.append(parts[index]+parts[index+1])
            index += 2
        else:
            result.append(parts[index])
            index += 1
    return result


def train_bpe(word_counts,merges=6):
    if not word_counts or merges < 0 or any(not word or count < 1 for word,count in word_counts.items()):
        raise ValueError("需非空单词和正计数")
    splits = {word:list(word) for word in word_counts}
    rules = []
    for step in range(merges):
        counts = Counter()
        for word,parts in splits.items():
            for pair in zip(parts,parts[1:]):
                counts[pair] += word_counts[word]
        if not counts:
            break
        # 并列按字典序处理，保证教学记录可复现。
        best = sorted(counts,key=lambda pair:(-counts[pair],pair))[0]
        rules.append({"step":step+1,"left":best[0],"right":best[1],"count":counts[best],"merged":best[0]+best[1]})
        splits = {word:merge_pair(parts,best) for word,parts in splits.items()}
    alphabet = sorted(set("".join(word_counts)))
    return rules,splits,alphabet


def tokenize_bpe(word,rules,alphabet):
    if not word or any(char not in alphabet for char in word):
        raise ValueError("本章简化BPE不覆盖该字符")
    parts = list(word)
    for rule in rules:
        parts = merge_pair(parts,(rule["left"],rule["right"]))
    return parts
