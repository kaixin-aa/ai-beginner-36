# 在用户自己的 PowerShell 窗口运行。不会向屏幕或项目文件写出密钥。
$ErrorActionPreference = 'Stop'
$taskApiSecret = Read-Host '粘贴 DeepSeek API Key，输入不会显示' -AsSecureString
$taskSecretPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($taskApiSecret)
try {
    $taskPlainSecret = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($taskSecretPointer)
    if ([string]::IsNullOrWhiteSpace($taskPlainSecret)) { throw '密钥为空，未保存' }
    [Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', $taskPlainSecret.Trim(), 'User')
    $env:DEEPSEEK_API_KEY = $taskPlainSecret.Trim()
    Write-Host '已保存为本机当前用户的 DEEPSEEK_API_KEY。没有写入项目。'
    Write-Host '可以在当前窗口运行问答；其他已经打开的程序可能需要重启。'
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($taskSecretPointer)
    $taskPlainSecret = $null
    $taskApiSecret.Dispose()
}
