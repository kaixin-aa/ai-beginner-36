# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## unknown_word

[错误文件](./examples/errors/unknown_word.py) 与 [修复文件](./examples/fixed/unknown_word.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\25-text-representation\examples\errors\unknown_word.py", line 5, in <module>
    print(tokenize_words("量子",load_data()["vectors"]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\25-text-representation\examples\text_core.py", line 25, in tokenize_words
    raise ValueError(f"词表未覆盖位置{position}的文字，需明确补充词或更换输入")
ValueError: 词表未覆盖位置0的文字，需明确补充词或更换输入
```

修复输出如下。

```text
['电脑']
任意新文字可先查看字符切分 ['量', '子']
字符切分成功不代表已拥有它们的向量
```

## zero_vector

[错误文件](./examples/errors/zero_vector.py) 与 [修复文件](./examples/fixed/zero_vector.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\25-text-representation\examples\errors\zero_vector.py", line 5, in <module>
    print(cosine([0,0],[1,0]))
          ^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\25-text-representation\examples\text_core.py", line 55, in cosine
    raise ValueError("零向量没有方向，不能计算余弦相似度")
ValueError: 零向量没有方向，不能计算余弦相似度
```

修复输出如下。

```text
零向量没有方向，不能计算余弦相似度
先补充有内容的表示，再计算 1.0
```
