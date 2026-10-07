# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## large_step

[错误文件](./examples/errors/large_step.py) 与 [修复文件](./examples/fixed/large_step.py)。

```text
损失变化 [37.0, 52.84]
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\16-math-intuition\examples\errors\large_step.py", line 9, in <module>
    assert rows[1]["loss"] < rows[0]["loss"], "步长过大，跨过最低点后走得太远"
AssertionError: 步长过大，跨过最低点后走得太远
```

修复输出如下。

```text
损失变化 [37.0, 13.96]
```

## wrong_direction

[错误文件](./examples/errors/wrong_direction.py) 与 [修复文件](./examples/fixed/wrong_direction.py)。

```text
更新前 w=9 loss=37.00
更新后 w=11.40 loss=71.56
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\16-math-intuition\examples\errors\wrong_direction.py", line 11, in <module>
    assert loss(new_w) < loss(w), "更新方向错误，损失没有下降"
AssertionError: 更新方向错误，损失没有下降
```

修复输出如下。

```text
更新前 w=9 loss=37.00
更新后 w=6.60 loss=13.96
```
