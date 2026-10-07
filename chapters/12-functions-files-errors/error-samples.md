# 错误示例与实际修复结果

以下内容由真实运行生成，日期为 2026 年 10 月 3 日。

## bad_encoding

错误文件为 [examples/errors/bad_encoding.py](./examples/errors/bad_encoding.py)，退出码为 1。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\12-functions-files-errors\examples\errors\bad_encoding.py", line 2, in <module>
    b"\xff\xfe".decode("utf-8")
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

修复文件为 [examples/fixed/bad_encoding.py](./examples/fixed/bad_encoding.py)，退出码为 0。

```text
内容不是有效的 UTF-8，请按原编码打开后另存为 UTF-8
```

## missing_file

错误文件为 [examples/errors/missing_file.py](./examples/errors/missing_file.py)，退出码为 1。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\12-functions-files-errors\examples\errors\missing_file.py", line 3, in <module>
    Path(__file__).with_name("not_created.txt").read_text(encoding="utf-8")
  File "G:\Python\Lib\pathlib.py", line 1027, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\pathlib.py", line 1013, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'G:\\002_work\\003_博客\\CSDN一万粉丝计划\\AI零基础36讲\\chapters\\12-functions-files-errors\\examples\\errors\\not_created.txt'
```

修复文件为 [examples/fixed/missing_file.py](./examples/fixed/missing_file.py)，退出码为 0。

```text
找不到输入文件，请检查路径
```
