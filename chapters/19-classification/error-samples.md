# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## input_shape

[错误文件](./examples/errors/input_shape.py) 与 [修复文件](./examples/fixed/input_shape.py)。

```text
G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\utils\validation.py:2749: UserWarning: X does not have valid feature names, but StandardScaler was fitted with feature names
  warnings.warn(
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\19-classification\examples\errors\input_shape.py", line 6, in <module>
    print(model.predict([5.1,3.5,1.4,.2]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\pipeline.py", line 788, in predict
    Xt = transform.transform(Xt)
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\utils\_set_output.py", line 316, in wrapped
    data_to_wrap = f(self, X, *args, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\preprocessing\_data.py", line 1075, in transform
    X = validate_data(
        ^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\utils\validation.py", line 2954, in validate_data
    out = check_array(X, input_name="X", **check_params)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\sklearn\utils\validation.py", line 1091, in check_array
    raise ValueError(msg)
ValueError: Expected 2D array, got 1D array instead:
array=[5.1 3.5 1.4 0.2].
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
```

修复输出如下。

```text
{'label': 0, 'name': 'setosa', 'probabilities': {'setosa': 0.9808127381969151, 'versicolor': 0.019186992121988183, 'virginica': 2.696810968691848e-07}}
```

## probability_order

[错误文件](./examples/errors/probability_order.py) 与 [修复文件](./examples/fixed/probability_order.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\19-classification\examples\errors\probability_order.py", line 5, in <module>
    assert wrong==classes[p.argmax()], '最大概率的位置不能当成类别编码'
AssertionError: 最大概率的位置不能当成类别编码
```

修复输出如下。

```text
类别 2 概率 0.7
```
