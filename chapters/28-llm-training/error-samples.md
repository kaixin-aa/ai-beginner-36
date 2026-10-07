# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## topk_range

[错误文件](./examples/errors/topk_range.py) 与 [修复文件](./examples/fixed/topk_range.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\28-llm-training\examples\errors\topk_range.py", line 6, in <module>
    print(generate(model,tokenizer,"小猫",top_k=100))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\27-transformer\examples\toy_transformer.py", line 155, in generate
    raise ValueError("top_k范围不正确")
ValueError: top_k范围不正确
```

修复输出如下。

```text
小猫吃鱼。 eos
```

## zero_temperature

[错误文件](./examples/errors/zero_temperature.py) 与 [修复文件](./examples/fixed/zero_temperature.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\28-llm-training\examples\errors\zero_temperature.py", line 5, in <module>
    print(probabilities_at_temperature([2,1,0],0))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\28-llm-training\examples\training_core.py", line 21, in probabilities_at_temperature
    raise ValueError("需要有限一维分数和有限正温度")
ValueError: 需要有限一维分数和有限正温度
```

修复输出如下。

```text
[0.866813 0.11731  0.015876]
需要确定性最高分时使用贪心选择，不将除数设为0
```
