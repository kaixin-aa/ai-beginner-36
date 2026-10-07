# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## context_limit

[错误文件](./examples/errors/context_limit.py) 与 [修复文件](./examples/fixed/context_limit.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\27-transformer\examples\errors\context_limit.py", line 6, in <module>
    print(generate(model,tokenizer,"小"*17))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\27-transformer\examples\toy_transformer.py", line 158, in generate
    raise ValueError("提示超过上下文上限")
ValueError: 提示超过上下文上限
```

修复输出如下。

```text
小猫吃 max_new_tokens
```

## unknown_character

[错误文件](./examples/errors/unknown_character.py) 与 [修复文件](./examples/fixed/unknown_character.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\27-transformer\examples\errors\unknown_character.py", line 6, in <module>
    print(tokenizer.encode("火星"))
          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\27-transformer\examples\toy_transformer.py", line 30, in encode
    raise ValueError("出现词表未覆盖的字符")
ValueError: 出现词表未覆盖的字符
```

修复输出如下。

```text
[1, 15, 20]
扩展词表还需调整并训练模型，不能只把未知字塞进输入
```
