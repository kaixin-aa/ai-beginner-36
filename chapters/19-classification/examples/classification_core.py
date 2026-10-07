"""四特征主实验与独立的两特征决策边界实验。"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from .project_core import FEATURES, TARGET_NAMES, load_dataset, train_project, make_model

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_FEATURES = FEATURES[2:]

def probability_result(model, frame):
    classes = np.asarray(model.classes_)
    probabilities = model.predict_proba(frame)
    if set(classes.tolist()) != {0, 1, 2}:
        raise ValueError('本章模型须包含三个 Iris 类别')
    if probabilities.shape != (len(frame),len(classes)) or not np.isfinite(probabilities).all():
        raise ValueError('概率形状或数值错误')
    if (probabilities < 0).any() or (probabilities > 1).any() or not np.allclose(probabilities.sum(axis=1),1):
        raise ValueError('每行类别概率应在零到一之间且合计为一')
    labels = classes[probabilities.argmax(axis=1)]
    return labels, probabilities, classes

def predict_one_with_proba(model, values):
    if isinstance(values,dict):
        if set(values) != set(FEATURES):
            raise ValueError('输入必须恰好包含四个测量字段')
        values = [values[f] for f in FEATURES]
    row = np.asarray(values,dtype=float)
    if row.shape != (4,) or not np.isfinite(row).all() or (row <= 0).any():
        raise ValueError('需要四个有限正数，单位为厘米')
    frame = pd.DataFrame([row],columns=FEATURES)
    labels, probabilities, classes = probability_result(model,frame)
    return {'label':int(labels[0]),'name':TARGET_NAMES[int(labels[0])],
            'probabilities':{TARGET_NAMES[int(k)]:float(p) for k,p in zip(classes,probabilities[0])}}

def experiment():
    model, train, test, summary = train_project()
    labels, probabilities, classes = probability_result(model,test[FEATURES])
    assert np.array_equal(labels,test.prediction.to_numpy())
    for i,label in enumerate(classes):
        test[f'p_{TARGET_NAMES[int(label)]}'] = probabilities[:,i]
    test['confidence'] = probabilities.max(axis=1)
    test['probability_gap'] = np.sort(probabilities,axis=1)[:,-1]-np.sort(probabilities,axis=1)[:,-2]
    matrix = confusion_matrix(test.target,labels,labels=[0,1,2])
    boundary_model = make_model().fit(train[BOUNDARY_FEATURES],train.target)
    summary.update({'confusion_matrix':matrix.tolist(),'classes':classes.astype(int).tolist(),
        'all_class_counts':load_dataset().target.value_counts().sort_index().astype(int).tolist(),
        'boundary_features':BOUNDARY_FEATURES,'boundary_test_accuracy':float(boundary_model.score(test[BOUNDARY_FEATURES],test.target)),
        'wrong_rows':test.loc[~test.correct].to_dict('records'),
        'lowest_gap_rows':test.sort_values('probability_gap').head(5).to_dict('records')})
    return model,boundary_model,train,test,summary
