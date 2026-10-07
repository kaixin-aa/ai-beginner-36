# 实际HTTP错误与修复

2026年10月4日，错误退出码1，修复退出码0。

## invalid_upload

[错误代码](./examples/errors/invalid_upload.py)与[修复代码](./examples/fixed/invalid_upload.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\35-web-deployment\examples\errors\invalid_upload.py", line 9, in <module>
    urlopen(request)
  File "G:\Python\Lib\urllib\request.py", line 215, in urlopen
    return opener.open(url, data, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 521, in open
    response = meth(req, response)
               ^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 630, in http_response
    response = self.parent.error(
               ^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 559, in error
    return self._call_chain(*args)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 492, in _call_chain
    result = func(*args)
             ^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 639, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 400: Bad Request
```

修复后输出。

```text
响应 200 导入 notes.txt
```

## missing_token

[错误代码](./examples/errors/missing_token.py)与[修复代码](./examples/fixed/missing_token.py)。

```text
Traceback (most recent call last):
  File "G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\35-web-deployment\examples\errors\missing_token.py", line 9, in <module>
    urlopen(request)
  File "G:\Python\Lib\urllib\request.py", line 215, in urlopen
    return opener.open(url, data, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 521, in open
    response = meth(req, response)
               ^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 630, in http_response
    response = self.parent.error(
               ^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 559, in error
    return self._call_chain(*args)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 492, in _call_chain
    result = func(*args)
             ^^^^^^^^^^^
  File "G:\Python\Lib\urllib\request.py", line 639, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 403: Forbidden
```

修复后输出。

```text
响应 200 导入 notes.txt
```
