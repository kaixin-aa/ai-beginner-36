# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## ambiguous_truth

[错误文件](./examples/errors/ambiguous_truth.py) 与 [修复文件](./examples/fixed/ambiguous_truth.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\13-numpy-vectors\examples\errors\ambiguous_truth.py", line 4, in <module>
    if scores >= 60:
       ^^^^^^^^^^^^
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

修复输出如下。

```text
每项及格 [True, False]
至少一项及格 True
全部及格 False
```

## bad_broadcast

[错误文件](./examples/errors/bad_broadcast.py) 与 [修复文件](./examples/fixed/bad_broadcast.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\13-numpy-vectors\examples\errors\bad_broadcast.py", line 4, in <module>
    print(scores + np.array([5, 2]))
          ~~~~~~~^~~~~~~~~~~~~~~~~~
ValueError: operands could not be broadcast together with shapes (2,3) (2,)
```

修复输出如下。

```text
[[85 70 92]
 [65 85 77]]
```
