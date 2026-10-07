# 第 10 章错误与修复记录

验证环境为 Windows 11 与 Python 3.12.2。下面三组错误均在本项目中实际运行，错误版本退出码为 1，修复版本退出码为 0。

## 字符串与整数相加

错误代码位于 examples/errors/string_number_type_error.py。

```text
Traceback (most recent call last):
  File "...string_number_type_error.py", line 2, in <module>
    print("总分钟数 " + total_minutes)
          ~~~~~~~~~~~~^~~~~~~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

修复文件位于 examples/fixed/string_number_fixed.py，实际输出如下。

```text
总分钟数 90
```

## 小数字符串转成整数

错误代码位于 examples/errors/invalid_int_conversion.py。

```text
Traceback (most recent call last):
  File "...invalid_int_conversion.py", line 1, in <module>
    minutes = int("90.5")
              ^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: '90.5'
```

修复文件位于 examples/fixed/invalid_int_fixed.py，实际输出如下。

```text
学习分钟数 90.5
```

## 变量名少写一个字母

错误代码位于 examples/errors/undefined_variable.py。

```text
Traceback (most recent call last):
  File "...undefined_variable.py", line 2, in <module>
    print(study_day)
          ^^^^^^^^^
NameError: name 'study_day' is not defined. Did you mean: 'study_days'?
```

修复文件位于 examples/fixed/undefined_variable_fixed.py，实际输出如下。

```text
学习天数 7
```

