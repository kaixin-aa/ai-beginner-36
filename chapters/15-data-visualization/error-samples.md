# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## mismatched_points

[错误文件](./examples/errors/mismatched_points.py) 与 [修复文件](./examples/fixed/mismatched_points.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\15-data-visualization\examples\errors\mismatched_points.py", line 5, in <module>
    plt.scatter([20, 15, 40], [1, 0])
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\matplotlib\_api\deprecation.py", line 453, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\matplotlib\pyplot.py", line 3948, in scatter
    __ret = gca().scatter(
            ^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\matplotlib\_api\deprecation.py", line 453, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\matplotlib\__init__.py", line 1524, in inner
    return func(
           ^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\matplotlib\axes\_axes.py", line 4936, in scatter
    raise ValueError("x and y must be the same size")
ValueError: x and y must be the same size
```

修复输出如下。

```text
配对时长 [20.0, 15.0, 40.0]
配对状态 [1, 0, 1]
横纵坐标数量一致 True
```
