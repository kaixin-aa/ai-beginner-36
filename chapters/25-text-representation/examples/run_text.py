import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from text_core import ROOT, load_data, sentence_vector, character_vectors, cosine, train_bpe, tokenize_bpe
from plot_style import configure_style, save_figure


def main():
    data = load_data()
    results,assets = ROOT/"results",ROOT/"assets"
    results.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    configure_style()
    characters,char_matrix = character_vectors(data["sentences"])
    encoded = [sentence_vector(text,data["vectors"]) for text in data["sentences"]]
    pairs = [{"left":i,"right":j,"case":case,"character_cosine":cosine(char_matrix[i],char_matrix[j]),"teaching_topic_cosine":cosine(encoded[i][0],encoded[j][0])} for i,j,case in data["pairs"]]
    rules,splits,alphabet = train_bpe(data["bpe_word_counts"])
    summary = {"provenance":data["provenance"],"embedding_learned":False,"sentences":[{"text":text,"tokens":tokens,"ids":ids,"vector":vector.tolist()} for text,(vector,tokens,ids) in zip(data["sentences"],encoded)],"character_vocabulary":characters,"pairs":pairs,"bpe_rules":rules,"bpe_splits":splits,"new_word_lowest":tokenize_bpe("lowest",rules,alphabet),"new_word_newlow":tokenize_bpe("newlow",rules,alphabet),"bpe_base":"Unicode characters; within supplied words only; not a byte-level or production tokenizer"}
    (results/"text-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for name,rows in [("similarity.csv",pairs),("bpe-merges.csv",rules)]:
        with (results/name).open("w",encoding="utf-8",newline="") as f:
            writer = csv.DictWriter(f,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    ax.axis("off")
    fig.suptitle("Token 是切分单位，编号用于查向量表",fontsize=23)
    ax.text(.03,.8,"原句   我用电脑学习Python",fontsize=21)
    ax.text(.03,.63,"字符   我 / 用 / 电 / 脑 / 学 / 习 / P / y / t / h / o / n",fontsize=16)
    ax.text(.03,.46,"词表   我 / 用 / 电脑 / 学习 / Python",fontsize=21)
    ax.text(.03,.28,"本章编号   "+" / ".join(map(str,encoded[0][2])),fontsize=20)
    ax.text(.03,.1,"查表后   5个Token × 4维向量 → 取均值得到4维句向量",fontsize=18)
    fig.text(.08,.045,"原创教学切分与编号；不同分词器有不同规则与词表，编号大小不表示含义远近",fontsize=12)
    save_figure(fig,assets,"token-example")
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.12,right=.95,top=.83,bottom=.28)
    positions = np.arange(len(pairs))
    ax.bar(positions-.18,[p["character_cosine"] for p in pairs],width=.36,label="字符计数",color="#5379b5")
    ax.bar(positions+.18,[p["teaching_topic_cosine"] for p in pairs],width=.36,label="人工主题向量",color="#38966c")
    ax.set(title="相似度跟随表示方式变化",ylabel="余弦相似度",ylim=(0,1.2),xticks=positions,xticklabels=["换词\n表达","共享电脑\n任务变化","主题\n无关","近义\n场景","否定\n事实改变"])
    ax.legend(loc="upper left",ncol=2,fontsize=14)
    ax.spines[["top","right"]].set_visible(False)
    fig.text(.08,.07,"原创句子与人工指定向量；主题结果由设定产生，不是预训练语义模型的性能测试\n否定句主题相似度仍为1，不能据此推断事实一致",fontsize=12)
    save_figure(fig,assets,"similarity-comparison")
    print(json.dumps({"pairs":pairs,"bpe_rules":rules,"newlow":summary["new_word_newlow"],"first_sentence":summary["sentences"][0]},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
