"""只在首次准备时复制第27章模型，已存在则拒绝覆盖。"""
import json
from pathlib import Path
import shutil
from training_core import ROOT,model_sha


def main():
    target = ROOT/"data/fixed-transformer.pt"
    if target.exists():
        raise SystemExit("快照已存在，复现请运行参数实验入口")
    source = ROOT.parent/"27-transformer/results/tiny-transformer.pt"
    target.parent.mkdir(exist_ok=True)
    shutil.copyfile(source,target)
    metadata = {"copied_on":"2026-10-03","source":"chapter27 locally trained 12-sentence model","sha256":model_sha(target),"trained_stages":["chapter27 next-token toy training only"],"instruction_finetuning_done":False,"preference_training_done":False}
    (ROOT/"data/baseline-metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(metadata["sha256"])


if __name__ == "__main__": main()
