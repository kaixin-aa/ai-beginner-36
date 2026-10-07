import csv
import json
from collections import Counter
import torch
import matplotlib.pyplot as plt
import numpy as np
from training_core import ROOT,load_teaching,load_baseline,probabilities_at_temperature,entropy,response_only_mask,generate,model_sha,F
from plot_style import configure_style,save_figure


def draw_flow(assets):
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    ax.set(xlim=(0,10),ylim=(0,6.25))
    ax.axis("off")
    stages = [(5.1,"语料准备\n来源、许可、去重、过滤和划分"),(3.8,"预训练\n从上下文预测下一Token，更新参数"),(2.5,"指令微调与偏好优化\n示范回答或比较记录，继续更新参数"),(1.2,"推理与生成\n读取参数，计算分数，选择下一Token")]
    for index,(y,text) in enumerate(stages):
        ax.text(5,y,text,ha="center",va="center",fontsize=17,bbox={"boxstyle":"round,pad=.35","fc":"#e5f4ed" if index==3 else "#e4eefb","ec":"#64748b"})
        if index<3:
            ax.annotate("",xy=(5,y-.91),xytext=(5,y-.46),arrowprops={"arrowstyle":"->","lw":1.7,"color":"#475569"})
    fig.suptitle("数据进入训练，固定参数进入推理",fontsize=23)
    fig.text(.07,.04,"原创概念图；常见路线示意，具体模型可有多轮后训练；本章未执行指令或偏好训练",fontsize=12)
    save_figure(fig,assets,"training-inference-flow")


def main():
    torch.set_num_threads(1)
    results,assets = ROOT/"results",ROOT/"assets"
    results.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    configure_style()
    teaching = load_teaching()
    model,tokenizer = load_baseline()
    before = {key:value.clone() for key,value in model.state_dict().items()}
    sha_before = model_sha(ROOT/"data/fixed-transformer.pt")
    temperature_rows = [{"temperature":temp,"probabilities":probabilities_at_temperature(teaching["temperature_logits"],temp).tolist(),"entropy_nats":entropy(probabilities_at_temperature(teaching["temperature_logits"],temp))} for temp in teaching["temperatures"]]
    experiments = []
    settings = [("sample_t05",.5,False,None),("sample_t10",1.,False,None),("sample_t20",2.,False,None),("sample_t20_top2",2.,False,2),("greedy_t20",2.,True,None)]
    for name,temp,greedy,top_k in settings:
        seeds = [42] if greedy else teaching["sample_seeds"]
        generations = [generate(model,tokenizer,teaching["sampling_prompt"],temperature=temp,seed=seed,greedy=greedy,top_k=top_k,max_new_tokens=12) for seed in seeds]
        counts = Counter(row["text"] for row in generations)
        experiments.append({"name":name,"temperature":temp,"greedy":greedy,"top_k":top_k,"runs":len(seeds),"unique_texts":len(counts),"eos_stops":sum(row["stop_reason"]=="eos" for row in generations),"counts":dict(counts),"generations":generations})
    x,y = response_only_mask(tokenizer,"我学","编程。")
    with torch.no_grad():
        scores = model(x)
        masked_loss = F.cross_entropy(scores.reshape(-1,model.vocab_size),y.reshape(-1),ignore_index=-100)
    pair = teaching["preference_pair"]
    totals = {name:sum(row["minutes"] for row in pair[name]) for name in ["chosen","rejected"]}
    summary = {"torch":str(torch.__version__),"baseline_sha256":sha_before,"baseline_file_unchanged":sha_before==model_sha(ROOT/"data/fixed-transformer.pt"),"parameters_unchanged":all(torch.equal(value,model.state_dict()[key]) for key,value in before.items()),"instruction_training_done":False,"preference_training_done":False,"temperature_teaching_logits":teaching["temperature_logits"],"temperature_rows":temperature_rows,"experiments":experiments,"response_mask_demo":{"prompt":"我学","response":"编程。","input_ids":x.tolist(),"targets":y.tolist(),"valid_response_targets":int((y!=-100).sum()),"loss_without_update":float(masked_loss)},"preference_minutes":totals,"total_generated_runs":sum(row["runs"] for row in experiments)}
    assert summary["parameters_unchanged"] and summary["baseline_file_unchanged"]
    (results/"parameter-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (results/"generation-comparison.csv").open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=["setting","temperature","top_k","seed","text","stop_reason"])
        writer.writeheader()
        writer.writerows({"setting":item["name"],"temperature":item["temperature"],"top_k":item["top_k"],"seed":row["seed"],"text":row["text"],"stop_reason":row["stop_reason"]} for item in experiments for row in item["generations"])
    draw_flow(assets)
    fig,ax = plt.subplots(figsize=(10,6.25),dpi=160)
    fig.subplots_adjust(left=.12,right=.95,top=.82,bottom=.23)
    positions = np.arange(3)
    for offset,row,color in zip([-.25,0,.25],temperature_rows,["#5379b5","#38966c","#db8a32"]):
        ax.bar(positions+offset,row["probabilities"],width=.25,label=f"温度 {row['temperature']:g}",color=color)
    ax.set(title="相同分数 [2,1,0]，不同温度改变分配",ylabel="Softmax分配",xticks=positions,xticklabels=["候选A","候选B","候选C"],ylim=(0,1))
    ax.legend()
    ax.spines[["top","right"]].set_visible(False)
    fig.text(.08,.055,"原创教学分数；按 logits / temperature 计算；没有改变模型参数，不能视为事实正确率",fontsize=12)
    save_figure(fig,assets,"temperature-probabilities")
    print(json.dumps({"parameters_unchanged":summary["parameters_unchanged"],"temperature_rows":temperature_rows,"experiments":[{k:v for k,v in row.items() if k!="generations"} for row in experiments],"response_mask_demo":summary["response_mask_demo"],"preference_minutes":totals},ensure_ascii=False,indent=2))


if __name__ == "__main__": main()
