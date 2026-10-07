# 实际错误与修复结果

运行日期为 2026 年 10 月 3 日，错误退出码均为 1，修复退出码均为 0。

## bad_column

[错误文件](./examples/errors/bad_column.py) 与 [修复文件](./examples/fixed/bad_column.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\indexes\base.py", line 3641, in get_loc
    return self._engine.get_loc(casted_key)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pandas/_libs/index.pyx", line 168, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 197, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 7668, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 7676, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'minute'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\14-pandas-data-cleaning\examples\errors\bad_column.py", line 4, in <module>
    print(frame["minute"])
          ~~~~~^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\frame.py", line 4378, in __getitem__
    indexer = self.columns.get_loc(key)
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\indexes\base.py", line 3648, in get_loc
    raise KeyError(key) from err
KeyError: 'minute'
```

修复输出如下。

```text
列名 ['minutes']
[20]
```

## bad_numeric

[错误文件](./examples/errors/bad_numeric.py) 与 [修复文件](./examples/fixed/bad_numeric.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\14-pandas-data-cleaning\examples\errors\bad_numeric.py", line 3, in <module>
    print(pd.Series(["20", "二十"]).astype(float))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\generic.py", line 6541, in astype
    new_data = self._mgr.astype(dtype=dtype, errors=errors)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\internals\managers.py", line 611, in astype
    return self.apply("astype", dtype=dtype, errors=errors)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\internals\managers.py", line 442, in apply
    applied = getattr(b, f)(**kwargs)
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\internals\blocks.py", line 607, in astype
    new_values = astype_array_safe(values, dtype, errors=errors)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\dtypes\astype.py", line 240, in astype_array_safe
    new_values = astype_array(values, dtype, copy=copy)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\dtypes\astype.py", line 182, in astype_array
    values = values.astype(dtype, copy=copy)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\review\.venv-data\Lib\site-packages\pandas\core\arrays\string_.py", line 940, in astype
    values = arr.astype(dtype)
             ^^^^^^^^^^^^^^^^^
ValueError: could not convert string to float: '二十'
```

修复输出如下。

```text
[20.0, nan]
无法转换 ['二十']
```
