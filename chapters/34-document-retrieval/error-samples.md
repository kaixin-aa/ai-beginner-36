# 实际错误与修复结果

2026年10月4日，错误退出码1，修复退出码0。

## image_pdf

[错误代码](./examples/errors/image_pdf.py)与[修复代码](./examples/fixed/image_pdf.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\34-document-retrieval\examples\errors\image_pdf.py", line 6, in <module>
    parse_document('image-only.pdf',(ROOT/'data/invalid/image-only.pdf').read_bytes())
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\projects\knowledge-assistant\knowledge_app\ingestion.py", line 31, in parse_document
    if not units:raise ValueError('没有可提取文字，扫描PDF请先另行处理')
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: 没有可提取文字，扫描PDF请先另行处理
```

修复输出。

```text
可提取文字页数 2 页码 [1, 2]
```

## stale_index

[错误代码](./examples/errors/stale_index.py)与[修复代码](./examples/fixed/stale_index.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\34-document-retrieval\examples\errors\stale_index.py", line 14, in <module>
    load_index(store,encoder)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\projects\knowledge-assistant\knowledge_app\indexing.py", line 57, in load_index
    if metadata['manifest']!=manifest(documents):raise ValueError('资料清单已变化，请更新索引')
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: 资料清单已变化，请更新索引
```

修复输出。

```text
索引已更新 片段 3 向量形状 (3, 512)
```
