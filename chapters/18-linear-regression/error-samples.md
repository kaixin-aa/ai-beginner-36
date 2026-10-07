# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## wrong_feature_count

[错误文件](./examples/errors/wrong_feature_count.py) 与 [修复文件](./examples/fixed/wrong_feature_count.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\18-linear-regression\examples\errors\wrong_feature_count.py", line 8, in <module>
    models["single"].predict(test[FEATURES])
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-mlcheck\Lib\site-packages\sklearn\linear_model\_base.py", line 298, in predict
    return self._decision_function(X)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-mlcheck\Lib\site-packages\sklearn\linear_model\_base.py", line 277, in _decision_function
    X = validate_data(self, X, accept_sparse=["csr", "csc", "coo"], reset=False)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-mlcheck\Lib\site-packages\sklearn\utils\validation.py", line 2929, in validate_data
    _check_feature_names(_estimator, X, reset=reset)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-mlcheck\Lib\site-packages\sklearn\utils\validation.py", line 2787, in _check_feature_names
    raise ValueError(message)
ValueError: The feature names should match those that were passed during fit.
Feature names unseen at fit time:
- curb_weight
- horsepower
```

修复输出如下。

```text
预测数量 40
前三条预测 [np.float64(12217.77), np.float64(25315.64), np.float64(16734.27)]
```
