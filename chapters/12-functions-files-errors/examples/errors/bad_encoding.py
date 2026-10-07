# 使用固定字节模拟非 UTF-8 内容，不涉及真实个人文件。
b"\xff\xfe".decode("utf-8")
