CELLS=[
('markdown','# 第 19 章花卉分类\n沿用第 17 章公开 Iris 快照。四特征主模型与两特征画图模型分开。'),
('code','from examples.classification_core import experiment, predict_one_with_proba\nfrom examples.project_core import FEATURES, TARGET_NAMES\nmodel,boundary,train,test,summary=experiment()\nprint("全部/训练/测试",summary["all_class_counts"],summary["train_class_counts"],summary["test_class_counts"])'),
('code','p=model.predict_proba(test[FEATURES])\nprint("类别列顺序",model.classes_)\nprint(p[:3])\nprint("每行合计",p[:3].sum(axis=1))'),
('code','print("测试正确",summary["test_correct"],"/",len(test))\nprint(summary["confusion_matrix"])'),
('code','print(test.loc[~test.correct,["sample_id","target","prediction","p_setosa","p_versicolor","p_virginica"]].to_string(index=False))'),
('code','print(predict_one_with_proba(model,[5.1,3.5,1.4,.2]))\nprint("两特征测试准确率",summary["boundary_test_accuracy"])'),
('code','from IPython.display import display, Image\nfor name in ["confusion-matrix","decision-boundary","wrong-probabilities"]:\n    display(Image(filename=f"assets/{name}.png",width=700))'),
('code','import numpy as np\nclasses=np.array([2,0,1]); probabilities=np.array([.7,.2,.1])\nprint("练习类别",classes[probabilities.argmax()])\nassert classes[probabilities.argmax()]==2'),
]
