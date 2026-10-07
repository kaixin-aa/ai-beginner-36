# 实际错误与修复结果

运行日期为 2026 年 10 月 4 日，错误退出码均为 1，修复退出码均为 0。

## invalid_parameter

[错误文件](./examples/errors/invalid_parameter.py) 与 [修复文件](./examples/fixed/invalid_parameter.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\errors\invalid_parameter.py", line 6, in <module>
    Config(api_key=FIXTURE_KEY, max_tokens=-1).payload("问题")
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\api_client.py", line 85, in payload
    self.validate()
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\api_client.py", line 80, in validate
    raise APIError("输出上限必须是正整数")
api_client.APIError: 输出上限必须是正整数
```

修复输出如下。

```text
有效输出上限 256
```

## missing_key

[错误文件](./examples/errors/missing_key.py) 与 [修复文件](./examples/fixed/missing_key.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\errors\missing_key.py", line 8, in <module>
    Config.from_env()
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\api_client.py", line 57, in from_env
    config.validate()
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\api_client.py", line 76, in validate
    raise APIError(f"未配置 {self.api_key_env}，请在本机设置环境变量")
api_client.APIError: 未配置 AI_TEACHING_MISSING_KEY，请在本机设置环境变量
```

修复输出如下。

```text
仅本地教学占位符 local_fixture 48
```

## rate_limit

[错误文件](./examples/errors/rate_limit.py) 与 [修复文件](./examples/fixed/rate_limit.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\errors\rate_limit.py", line 7, in <module>
    ask(Config(base_url=base, api_key=FIXTURE_KEY, fixture_http=True), "问题")
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api\examples\api_client.py", line 150, in ask
    raise APIError(f"HTTP {status}，{hint}") from None
api_client.APIError: HTTP 429，请求过快，请稍后手动重试
```

修复输出如下。

```text
HTTP 429，请求过快，请稍后手动重试
已结束本次调用，没有自动重试；本地服务收到 1 次请求
```
