# 在本机配置 DeepSeek

你已经在 DeepSeek 开发平台充值，接下来需要创建 API Key，并让电脑上的问答程序读取它。整个过程无需把密钥发到聊天里。

## 创建密钥

打开 [DeepSeek 开发平台](https://platform.deepseek.com/)，登录已充值的账号。在 API Key 管理入口创建密钥，并复制它。平台界面文字可能调整，按实际页面寻找 API Key 管理入口即可。

## 在自己的 PowerShell 窗口输入

打开 Windows PowerShell，切换到本章目录。

```powershell
Set-Location -LiteralPath 'G:\002_work\003_博客\CSDN一万粉丝计划\AI零基础36讲\chapters\29-first-api'
.\configure-key.ps1
```

看到“粘贴 DeepSeek API Key，输入不会显示”后粘贴密钥，再按回车。屏幕没有显示完整字符是预期行为。脚本会保存为本机当前用户的 `DEEPSEEK_API_KEY` 环境变量，不创建密钥文件。

如果当前窗口提示禁止运行脚本，可先仅调整当前 PowerShell 进程，再重试。关闭窗口后该进程设置结束。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\configure-key.ps1
```

在同一窗口中检查是否已配置，只显示真假。

```powershell
-not [string]::IsNullOrWhiteSpace($env:DEEPSEEK_API_KEY)
```

结果应为 `True`。不要运行显示环境变量完整值的命令，也不要发送密钥截图。此设置为本机用户环境变量，同一用户的其他程序可能读取它。

## 发出一条短请求

本章默认提供方为 DeepSeek，模型为 `deepseek-flash`，短输出上限为 256。模型名已核对 2026 年 10 月 4 日的官方文档。若提示模型不可用，再按平台文档调整 `AI_MODEL`。

```powershell
py -3.12 examples/qa.py "用一句话解释 API"
```

程序会显示“真实 API 响应”、回答和用量，并保存名称以 `live_api-` 开头的 JSON 文件。请求会使用平台余额，本章默认只发送一次，不自动重试。

如果只是希望配置好后由当前项目继续验收，完成隐藏输入后告诉助手“已在本机配置”。已经打开的程序可能尚未读取新环境，验收时可只读取当前用户的这个变量，不输出值。无须把密钥再发给助手。

## 更换配置

[环境变量模板](./.env.example)列出全部配置名称，只是说明文件，程序不会自动读取。以下命令可以在当前 PowerShell 会话调整输出上限和超时。

```powershell
$env:AI_MAX_TOKENS = '256'
$env:AI_TIMEOUT_SECONDS = '30'
```

本机教学服务使用固定占位符和回环地址，入口为 `examples/run_fixture.py`。这个入口不消耗平台余额，也不运行模型，输出不能用作真实调用验收。
