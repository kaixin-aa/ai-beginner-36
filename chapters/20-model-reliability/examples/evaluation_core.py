"""只在既有训练部分交叉验证，历史测试分数只作教学复核。"""
from pathlib import Path
import importlib.util
import numpy as np
from sklearn.base import clone
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,mean_absolute_error
from sklearn.model_selection import KFold,StratifiedKFold,train_test_split
from sklearn.tree import DecisionTreeClassifier
ROOT=Path(__file__).resolve().parents[1]
CHAPTERS=ROOT.parent


def dependency(name,file,module_name):
    spec=importlib.util.spec_from_file_location(module_name,CHAPTERS/name/'examples'/file)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

iris=dependency('19-classification','project_core.py','ch19_project')
auto=dependency('18-linear-regression','regression_core.py','ch18_regression')
SPAM_Y=np.array([1,1,1,1,0,0,0,0,0,0])
SPAM_P=np.array([.9,.8,.4,.2,.7,.45,.3,.1,.05,.01])


def binary_report(y,pred):
    y=np.asarray(y)
    pred=np.asarray(pred)
    if y.ndim!=1 or pred.shape!=y.shape or len(y)==0 or not np.isin(y,[0,1]).all() or not np.isin(pred,[0,1]).all():
        raise ValueError('真实值与预测值必须是非空等长的一维二分类编码')
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp),
        'accuracy':float(accuracy_score(y,pred)),'precision':float(precision_score(y,pred,zero_division=0)),
        'recall':float(recall_score(y,pred,zero_division=0)),'F1':float(f1_score(y,pred,zero_division=0))}


def threshold_report(threshold):
    if not np.isfinite(threshold) or not 0<=threshold<=1:
        raise ValueError('阈值须在零到一之间')
    return {'threshold':float(threshold),**binary_report(SPAM_Y,(SPAM_P>=threshold).astype(int))}


def fold_scores(model,x,y,folds,task):
    x=np.asarray(x); y=np.asarray(y)
    records=[]
    for number,(train,val) in enumerate(folds.split(x,y),start=1):
        fitted=clone(model).fit(x[train],y[train])
        predictions=fitted.predict(x[val])
        score=accuracy_score(y[val],predictions) if task=='classification' else mean_absolute_error(y[val],predictions)
        records.append({'fold':number,'train_positions':train.tolist(),'validation_positions':val.tolist(),'score':float(score)})
    return records


def evaluate_existing():
    frame=iris.load_dataset(); train,test=iris.split_dataset(frame)
    candidates={'baseline':DummyClassifier(strategy='most_frequent'),
        'logistic':iris.make_model(),'tree_depth1':DecisionTreeClassifier(max_depth=1,random_state=42),
        'tree_full':DecisionTreeClassifier(random_state=42)}
    rows=[]; manifests={}
    folds=StratifiedKFold(n_splits=5,shuffle=True,random_state=7)
    for name,model in candidates.items():
        records=fold_scores(model,train[iris.FEATURES],train.target,folds,'classification')
        fitted=clone(model).fit(train[iris.FEATURES],train.target)
        scores=np.array([r['score'] for r in records])
        rows.append({'task':'classification','model':name,'metric':'accuracy','train_score':float(fitted.score(train[iris.FEATURES],train.target)),
            'cv_mean':float(scores.mean()),'cv_std':float(scores.std(ddof=0)),
            'historical_test_score':float(fitted.score(test[iris.FEATURES],test.target))})
        manifests['iris_'+name]={'outer_train_ids':train.sample_id.tolist(),'outer_test_ids':test.sample_id.tolist(),'folds':records}
    clean,_,_=auto.prepare_data(); train,test=auto.split_data(clean)
    folds=KFold(n_splits=5,shuffle=True,random_state=7)
    for name,model,fields in [('baseline',DummyRegressor(strategy='mean'),['engine_size']),('single',LinearRegression(),['engine_size']),('multi',LinearRegression(),auto.FEATURES)]:
        records=fold_scores(model,train[fields],train.price,folds,'regression')
        fitted=clone(model).fit(train[fields],train.price)
        scores=np.array([r['score'] for r in records])
        rows.append({'task':'regression','model':name,'metric':'MAE','train_score':float(mean_absolute_error(train.price,fitted.predict(train[fields]))),
            'cv_mean':float(scores.mean()),'cv_std':float(scores.std(ddof=0)),
            'historical_test_score':float(mean_absolute_error(test.price,fitted.predict(test[fields])))})
        manifests['auto_'+name]={'outer_train_ids':train.sample_id.tolist(),'outer_test_ids':test.sample_id.tolist(),'folds':records}
    return rows,manifests


def leakage_experiment():
    # 原创教学实验，标签由随机数生成，与六列噪声特征没有设定关系。
    rng=np.random.default_rng(7)
    x=rng.normal(size=(400,6)); y=rng.integers(0,2,size=400)
    ids=np.arange(400)
    train,test=train_test_split(ids,test_size=.25,random_state=42,stratify=y)
    clean=DecisionTreeClassifier(random_state=42).fit(x[train],y[train])
    # 错误流程把标签复制进特征，连测试标签也一起复制。
    leaked=np.column_stack([x,y])
    bad=DecisionTreeClassifier(random_state=42).fit(leaked[train],y[train])
    return {'source':'原创随机噪声教学实验','seed':7,'train_rows':len(train),'test_rows':len(test),
        'clean_train_accuracy':float(clean.score(x[train],y[train])),
        'clean_test_accuracy':float(clean.score(x[test],y[test])),
        'leaked_train_accuracy':float(bad.score(leaked[train],y[train])),
        'leaked_test_accuracy':float(bad.score(leaked[test],y[test])),
        'train_ids':train.tolist(),'test_ids':test.tolist(),
        'clean_predictions':clean.predict(x[test]).tolist(),'leaked_predictions':bad.predict(leaked[test]).tolist(),
        'test_labels':y[test].tolist(),'clean_features':6,'leaked_features':7}
