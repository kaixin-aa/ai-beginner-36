# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## freeze_everything

[错误文件](./examples/errors/freeze_everything.py) 与 [修复文件](./examples/fixed/freeze_everything.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\24-convolution-transfer\examples\errors\freeze_everything.py", line 11, in <module>
    loss.backward()
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\_tensor.py", line 625, in backward
    torch.autograd.backward(
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\autograd\__init__.py", line 354, in backward
    _engine_run_backward(
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\autograd\graph.py", line 841, in _engine_run_backward
    return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

修复输出如下。

```text
特征梯度为空 True
新分类头有梯度 True
```

## old_head

[错误文件](./examples/errors/old_head.py) 与 [修复文件](./examples/fixed/old_head.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\24-convolution-transfer\examples\errors\old_head.py", line 8, in <module>
    assert output.shape[1] == 2, "目标只有even和odd，必须替换十类源分类头"
AssertionError: 目标只有even和odd，必须替换十类源分类头
```

修复输出如下。

```text
(1, 2)
```
