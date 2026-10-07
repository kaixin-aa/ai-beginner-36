# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## all_masked

[错误文件](./examples/errors/all_masked.py) 与 [修复文件](./examples/fixed/all_masked.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\26-attention\examples\errors\all_masked.py", line 6, in <module>
    print(softmax_rows([[-np.inf,-np.inf]]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\26-attention\examples\attention_core.py", line 17, in softmax_rows
    raise ValueError("不能把某一行的所有位置都屏蔽")
ValueError: 不能把某一行的所有位置都屏蔽
```

修复输出如下。

```text
[[1. 0.]]
```

## no_transpose

[错误文件](./examples/errors/no_transpose.py) 与 [修复文件](./examples/fixed/no_transpose.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\26-attention\examples\errors\no_transpose.py", line 4, in <module>
    print(q@k)
          ~^~
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 4 is different from 2)
```

修复输出如下。

```text
(4, 4)
```
