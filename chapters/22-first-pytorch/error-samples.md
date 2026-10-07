# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## accumulated_gradient

[错误文件](./examples/errors/accumulated_gradient.py) 与 [修复文件](./examples/fixed/accumulated_gradient.py)。

```text
梯度 60.0
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\22-first-pytorch\examples\errors\accumulated_gradient.py", line 5, in <module>
    assert w.grad.item()==30,'前一轮梯度没有清除'
AssertionError: 前一轮梯度没有清除
```

修复输出如下。

```text
每轮清除后的梯度 30.0
```

## disabled_grad

[错误文件](./examples/errors/disabled_grad.py) 与 [修复文件](./examples/fixed/disabled_grad.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\22-first-pytorch\examples\errors\disabled_grad.py", line 4, in <module>
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
损失 25.0 梯度 30.0
```

## integer_input

[错误文件](./examples/errors/integer_input.py) 与 [修复文件](./examples/fixed/integer_input.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\22-first-pytorch\examples\errors\integer_input.py", line 4, in <module>
    print(model(x))
          ^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-torch\Lib\site-packages\torch\nn\modules\linear.py", line 134, in forward
    return F.linear(input, self.weight, self.bias)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: mat1 and mat2 must have the same dtype, but got Long and Float
```

修复输出如下。

```text
tensor([[3.],
        [5.]])
```
