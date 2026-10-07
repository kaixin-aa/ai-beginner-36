import csv
import json
import torch
import matplotlib.pyplot as plt
from toy_transformer import ROOT,train_model,save_model,load_model,generate,make_batch,load_corpus
from plot_style import configure_style,new_figure,save_figure


def draw_structure(assets,vocab):
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    ax.set(xlim=(0,10),ylim=(0,10))
    ax.axis("off")
    blocks = [(9.3,"Token编号 B×T"),(8.25,"词嵌入 + 位置嵌入   B×T×16"),(7.1,"LayerNorm → 因果两头注意力"),(5.95,"注意力投影 + 原输入   B×T×16"),(4.8,"LayerNorm → 前馈 16→32→16"),(3.65,"前馈输出 + 原输入   B×T×16"),(2.5,"最终 LayerNorm → 词表投影"),(1.35,f"类别分数 B×T×{vocab} → 选择下一Token")]
    for index,(y,text) in enumerate(blocks):
        ax.text(5,y,text,ha="center",va="center",fontsize=14,bbox={"boxstyle":"round,pad=.3","fc":"#e5f4ed" if index in [3,5] else "#e4eefb","ec":"#64748b"})
        if index<len(blocks)-1:
            ax.annotate("",xy=(5,y-.84),xytext=(5,y-.34),arrowprops={"arrowstyle":"->","lw":1.6,"color":"#475569"})
    fig.suptitle("本章单层 Transformer 的输入输出",fontsize=23)
    fig.text(.06,.045,"原创结构图；从上向下计算；前置归一化；仅解码器式因果主线，无交叉注意力",fontsize=12)
    save_figure(fig,assets,"transformer-structure")


def main():
    results,assets = ROOT/"results",ROOT/"assets"
    results.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    configure_style()
    model,tokenizer,history,summary = train_model()
    save_model(model,tokenizer,results/"tiny-transformer.pt")
    loaded,saved_tokenizer = load_model(results/"tiny-transformer.pt")
    x,y = make_batch(load_corpus()["sentences"],tokenizer)
    with torch.no_grad():
        summary["reload_logits_identical"] = torch.equal(model(x),loaded(x))
        demo = torch.tensor([tokenizer.encode("小猫",bos=True)],dtype=torch.long)
        _,summary["module_shapes"] = loaded(demo,trace=True)
    generations = [generate(loaded,saved_tokenizer,prompt) for prompt in load_corpus()["prompts"]]
    summary["generations"] = generations
    (results/"transformer-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (results/"vocabulary.json").write_text(json.dumps(tokenizer.tokens,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (results/"loss-history.csv").open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=["step","train_loss"])
        writer.writeheader()
        writer.writerows(history)
    rows = [{"prompt":result["prompt"],"step":row["step"],"prefix_before":row["prefix_before"],"input_tokens":row["input_tokens"],"selected_token":row["selected_token"],"probability":row["selected_probability"]} for result in generations for row in result["trace"]]
    with (results/"generation-steps.csv").open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    draw_structure(assets,len(tokenizer.tokens))
    fig,ax = new_figure("十二条教学短句的下一Token训练", "参数更新次数", "训练交叉熵", "原创虚构语料；完整训练集参与每次更新；没有独立测试，不能作为泛化成绩")
    ax.plot([row["step"] for row in history],[row["train_loss"] for row in history],color="#5379b5",linewidth=2.4)
    save_figure(fig,assets,"training-loss")
    print(json.dumps({k:v for k,v in summary.items() if k not in ["generations","module_shapes"]},ensure_ascii=False,indent=2))
    print([(result["prompt"],result["text"],result["stop_reason"]) for result in generations])


if __name__ == "__main__": main()
