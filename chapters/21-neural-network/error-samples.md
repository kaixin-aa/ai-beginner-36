# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## elementwise

[错误文件](./examples/errors/elementwise.py) 与 [修复文件](./examples/fixed/elementwise.py)。

```text
[[ 0.5 -2. ]
 [ 1.   1. ]]
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\21-neural-network\examples\errors\elementwise.py", line 5, in <module>
    assert wrong.shape==(2,),'逐元素乘法没有计算每个隐藏节点的加权和'
AssertionError: 逐元素乘法没有计算每个隐藏节点的加权和
```

修复输出如下。

```text
形状 (2,) 结果 [ 2.5 -0.5]
```

## matrix_shape

[错误文件](./examples/errors/matrix_shape.py) 与 [修复文件](./examples/fixed/matrix_shape.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\21-neural-network\examples\errors\matrix_shape.py", line 3, in <module>
    print(x@weights)
          ~^~~~~~~~
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 3 is different from 2)
```

修复输出如下。

```text
[ 2.5 -0.5]
```
