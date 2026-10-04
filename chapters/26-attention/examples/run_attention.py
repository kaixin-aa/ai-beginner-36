import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from attention_core import ROOT,load_data,run_heads
from plot_style import configure_style,save_figure


def main():
    results,assets = ROOT/"results",ROOT/"assets"
    results.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    configure_style()
    data = load_data()
    heads,concatenated,output = run_heads(data)
    causal_heads,_,causal_output = run_heads(data,True)
    summary = {"provenance":data["provenance"],"tokens":data["tokens"],"x":data["x"],"heads":[{key:value.tolist() for key,value in head.items()} for head in heads],"concatenated":concatenated.tolist(),"output_projection":output.tolist(),"causal_weights":[head["weights"].tolist() for head in causal_heads],"causal_output_projection":causal_output.tolist(),"row_sums":[head["weights"].sum(1).tolist() for head in heads],"head_shapes":{"q":[4,2],"k":[4,2],"v":[4,2],"scores":[4,4],"weights":[4,4],"output":[4,2]},"multihead_shapes":{"concatenated":[4,4],"wo":[4,4],"projected_output":[4,4]}}
    (results/"attention-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rows = [{"key_token":token,"raw_score":float(heads[0]["raw"][2,i]),"scaled_score":float(heads[0]["scaled"][2,i]),"weight":float(heads[0]["weights"][2,i]),"v0":float(heads[0]["v"][i,0]),"v1":float(heads[0]["v"][i,1]),"contribution0":float(heads[0]["weights"][2,i]*heads[0]["v"][i,0]),"contribution1":float(heads[0]["weights"][2,i]*heads[0]["v"][i,1])} for i,token in enumerate(data["tokens"])]
    with (results/"pronoun-steps.csv").open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for number,head in enumerate(heads,start=1):
        for key in ["q","k","v","raw","scaled","weights","output"]:
            np.savetxt(results/f"head{number}-{key}.csv",head[key],delimiter=",",fmt="%.12f")
    fig,axes = plt.subplots(1,2,figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.1,right=.95,top=.78,bottom=.23,wspace=.45)
    for number,(ax,head) in enumerate(zip(axes,heads),start=1):
        ax.imshow(head["weights"],vmin=0,vmax=1,cmap="Blues")
        ax.set(title=f"头 {number}",xticks=range(4),xticklabels=data["tokens"],yticks=range(4),yticklabels=data["tokens"],xlabel="K、V 对应位置",ylabel="Q 对应位置")
        ax.tick_params(labelsize=13)
        for (r,c),value in np.ndenumerate(head["weights"]):
            ax.text(c,r,f"{value:.3f}",ha="center",va="center",fontsize=13,color="white" if value>.55 else "black")
    fig.suptitle("两个头使用不同投影，得到不同权重",fontsize=23)
    fig.text(.08,.055,"原创教学矩阵；每行权重和为1；未训练模型，不代表实际语言模型对词语的判断",fontsize=12)
    save_figure(fig,assets,"attention-matrices")
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    ax.set(xlim=(0,10),ylim=(0,6.25))
    ax.axis("off")
    weights = heads[0]["weights"][2]
    for x,token,weight in zip([1.1,3.7,6.3,8.9],data["tokens"],weights):
        ax.text(x,4.4,f"{token}\n{weight:.4f}",ha="center",va="center",fontsize=19,bbox={"boxstyle":"round,pad=.4","fc":"#e4eefb","ec":"#64748b"})
        ax.annotate("",xy=(x,3.8),xytext=(5,1.5),arrowprops={"arrowstyle":"->","lw":1+5*weight,"color":"#5379b5"})
    ax.text(5,1.15,"头1的 Q\n当前位置“它”",ha="center",va="center",fontsize=20,bbox={"boxstyle":"round,pad=.4","fc":"#e5f4ed","ec":"#64748b"})
    fig.suptitle("“它”这一行，按权重汇总各位置的 V",fontsize=23)
    fig.text(.08,.055,"箭头从当前Q位置指向提供K、V的位置；粗细表示权重；所有数值为人工教学设定",fontsize=12)
    save_figure(fig,assets,"attention-links")
    print(json.dumps({"pronoun_raw":heads[0]["raw"][2].tolist(),"pronoun_weights":weights.tolist(),"pronoun_output":heads[0]["output"][2].tolist(),"head2_weights":heads[1]["weights"][2].tolist(),"causal_pronoun_weights":causal_heads[0]["weights"][2].tolist(),"concat_shape":list(concatenated.shape)},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
