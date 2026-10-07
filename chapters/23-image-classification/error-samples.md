# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## float_labels

[错误文件](./examples/errors/float_labels.py) 与 [修复文件](./examples/fixed/float_labels.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\23-image-classification\examples\errors\float_labels.py", line 6, in <module>
    print(nn.CrossEntropyLoss()(logits, labels))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\loss.py", line 1385, in forward
    return F.cross_entropy(
           ^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\functional.py", line 3458, in cross_entropy
    return torch._C._nn.cross_entropy_loss(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: expected scalar type Long but found Float
```

修复输出如下。

```text
交叉熵 0.407606
```

## wrong_size

[错误文件](./examples/errors/wrong_size.py) 与 [修复文件](./examples/fixed/wrong_size.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\23-image-classification\examples\errors\wrong_size.py", line 7, in <module>
    pixels_to_tensor(np.zeros((28, 28)))
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\23-image-classification\examples\image_core.py", line 36, in pixels_to_tensor
    raise ValueError("需要非空的8×8像素矩阵或一批矩阵")
ValueError: 需要非空的8×8像素矩阵或一批矩阵
```

修复输出如下。

```text
输入形状 (1, 1, 8, 8)
```
