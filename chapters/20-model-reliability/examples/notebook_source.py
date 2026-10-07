CELLS=[
('markdown','# 第 20 章评估实验\n公开汽车与 Iris 沿用前章。垃圾信息概率、类别不平衡与泄漏实验为原创教学设定。历史测试部分仅作复核。'),
('code','from examples.evaluation_core import evaluate_existing, threshold_report, binary_report, leakage_experiment\nimport pandas as pd\nrows,manifest=evaluate_existing()\nprint(pd.DataFrame(rows).to_string(index=False))'),
('code','first=manifest["iris_logistic"]\nprint("外层训练/测试",len(first["outer_train_ids"]),len(first["outer_test_ids"]))\nfor fold in first["folds"]:\n    print(fold["fold"],len(fold["train_positions"]),len(fold["validation_positions"]),fold["score"])'),
('code','print(pd.DataFrame([threshold_report(.5),threshold_report(.25)]).to_string(index=False))'),
('code','print(binary_report([0]*95+[1]*5,[0]*100))'),
('code','leak=leakage_experiment()\nprint({k:v for k,v in leak.items() if not isinstance(v,list)})'),
('code','from IPython.display import display,Image\nfor name in ["overfitting-comparison","leakage-demo"]:\n    display(Image(filename=f"assets/{name}.png",width=700))'),
('code','report=binary_report([1,1,1,0,0],[1,0,1,1,0])\nprint(report)\nassert report["TP"]==2 and report["FP"]==1 and report["FN"]==1'),
]
