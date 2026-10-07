# 错误示例与实际修复结果

以下内容由真实运行生成，日期为 2026 年 10 月 3 日。

## bad_container

错误文件为 [examples/errors/bad_container.py](./examples/errors/bad_container.py)，退出码为 1。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\11-control-flow-containers\examples\errors\bad_container.py", line 2, in <module>
    for record in records:
TypeError: 'int' object is not iterable
```

修复文件为 [examples/fixed/bad_container.py](./examples/fixed/bad_container.py)，退出码为 0。

```text
输入错误，请提供列表
```

## bad_index

错误文件为 [examples/errors/bad_index.py](./examples/errors/bad_index.py)，退出码为 1。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\11-control-flow-containers\examples\errors\bad_index.py", line 2, in <module>
    print(topics[0])
          ~~~~~~^^^
IndexError: list index out of range
```

修复文件为 [examples/fixed/bad_index.py](./examples/fixed/bad_index.py)，退出码为 0。

```text
还没有学习项目
```

## missing_key

错误文件为 [examples/errors/missing_key.py](./examples/errors/missing_key.py)，退出码为 1。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\11-control-flow-containers\examples\errors\missing_key.py", line 2, in <module>
    print(record["done"])
          ~~~~~~^^^^^^^^
KeyError: 'done'
```

修复文件为 [examples/fixed/missing_key.py](./examples/fixed/missing_key.py)，退出码为 0。

```text
缺少完成状态，请补充记录
```
