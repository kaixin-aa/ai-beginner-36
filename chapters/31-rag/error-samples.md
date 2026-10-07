# 实际错误与修复结果

运行日期为 2026 年 10 月 4 日，错误退出码均为 1，修复退出码均为 0。

## fabricated_citation

[错误文件](./examples/errors/fabricated_citation.py) 与 [修复文件](./examples/fixed/fabricated_citation.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\31-rag\examples\errors\fabricated_citation.py", line 5, in <module>
    validate_answer('{"status":"answered","answer":"借30天","citations":[{"chunk_id":"不存在","quote":"借30天"}]}',[])
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\31-rag\examples\rag_answer.py", line 37, in validate_answer
    raise ValueError("引用编号或原文无法对应检索片段")
ValueError: 引用编号或原文无法对应检索片段
```

修复输出如下。

```text
[{'chunk_id': 'demo@0-7', 'quote': '书籍可以借14天。', 'source': 'demo.txt', 'line_start': 1, 'line_end': 1, 'quote_start': 0, 'quote_end': 9}]
```

## invalid_overlap

[错误文件](./examples/errors/invalid_overlap.py) 与 [修复文件](./examples/fixed/invalid_overlap.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\31-rag\examples\errors\invalid_overlap.py", line 5, in <module>
    split_text("示例资料","demo.txt",4,4)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\31-rag\examples\retrieval.py", line 10, in split_text
    raise ValueError("重叠必须小于正整数块长度")
ValueError: 重叠必须小于正整数块长度
```

修复输出如下。

```text
['abcdef', 'efghij']
```
