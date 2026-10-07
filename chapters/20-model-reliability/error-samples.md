# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## leaked_feature

[错误文件](./examples/errors/leaked_feature.py) 与 [修复文件](./examples/fixed/leaked_feature.py)。

```text
含答案列的测试准确率 1.0
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\20-model-reliability\examples\errors\leaked_feature.py", line 7, in <module>
    assert r['leaked_features']==r['clean_features'],'检查失败，特征包含预测时拿不到的答案'
AssertionError: 检查失败，特征包含预测时拿不到的答案
```

修复输出如下。

```text
移除答案列的测试准确率 0.52
```

## no_positive

[错误文件](./examples/errors/no_positive.py) 与 [修复文件](./examples/fixed/no_positive.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\20-model-reliability\examples\errors\no_positive.py", line 3, in <module>
    print(true_positive/(true_positive+false_positive))
          ~~~~~~~~~~~~~^^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

修复输出如下。

```text
{'TN': 1, 'FP': 0, 'FN': 1, 'TP': 0, 'accuracy': 0.5, 'precision': 0.0, 'recall': 0.0, 'F1': 0.0}
```
