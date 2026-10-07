try:
    text = b"\xff\xfe".decode("utf-8")
except UnicodeDecodeError:
    print("内容不是有效的 UTF-8，请按原编码打开后另存为 UTF-8")
else:
    print(text)
