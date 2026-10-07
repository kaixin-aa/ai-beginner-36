# 实际错误与修复结果

运行日期为 2026 年 10 月 4 日，错误退出码均为 1，修复退出码均为 0。

## unknown_tool

[错误文件](./examples/errors/unknown_tool.py) 与 [修复文件](./examples/fixed/unknown_tool.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\32-tools-agent\examples\errors\unknown_tool.py", line 5, in <module>
    dispatch("write_file",{"path":"demo.txt"},lambda _:None)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\32-tools-agent\examples\tools.py", line 53, in dispatch
    if name not in("calculate","search_documents"):raise ValueError("工具未获授权")
                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: 工具未获授权
```

修复输出如下。

```text
{'value': 51}
```

## unsafe_expression

[错误文件](./examples/errors/unsafe_expression.py) 与 [修复文件](./examples/fixed/unsafe_expression.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\32-tools-agent\examples\errors\unsafe_expression.py", line 6, in <module>
    calculate("open('demo.txt','w')")
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\32-tools-agent\examples\tools.py", line 37, in calculate
    return {"value":evaluate(tree.body)}
                    ^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\32-tools-agent\examples\tools.py", line 34, in evaluate
    else:raise ValueError("只允许数值、括号和加减乘除")
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: 只允许数值、括号和加减乘除
```

修复输出如下。

```text
{'value': 21}
```
