# 实际错误与修复结果

2026年10月4日运行，错误退出码1，修复退出码0。

## empty_question

[错误代码](./examples/errors/empty_question.py)与[修复代码](./examples/fixed/empty_question.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\33-project-design\examples\errors\empty_question.py", line 5, in <module>
    AskRequest('   ')
  File "<string>", line 4, in __init__
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\projects\knowledge-assistant\knowledge_app\contracts.py", line 46, in __post_init__
    raise ValueError("问题必须为1至300字符")
ValueError: 问题必须为1至300字符
```

修复后输出。

```text
柳叶学习室周一开放吗？
```

## upload_path

[错误代码](./examples/errors/upload_path.py)与[修复代码](./examples/fixed/upload_path.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\33-project-design\examples\errors\upload_path.py", line 5, in <module>
    FilePolicy().validate('../secret.txt',10)
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\projects\knowledge-assistant\knowledge_app\contracts.py", line 16, in validate
    raise ValueError("只接收文件名，不接收路径")
ValueError: 只接收文件名，不接收路径
```

修复后输出。

```text
.txt
```
