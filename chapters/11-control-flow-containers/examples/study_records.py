"""教学用虚构学习记录。直接修改 records，再运行本文件。"""

records = [
    {"title": "变量", "done": True, "minutes": 20},
    {"title": "循环", "done": False, "minutes": 15},
    {"title": "列表", "done": True, "minutes": 25},
    {"title": "字典", "minutes": 10},
    {"title": "集合", "done": "False", "minutes": 5},
    "这条记录格式不对",
]

# 本章先使用顺序执行的代码，第 12 章再整理成函数。
completed = 0
pending = []
invalid = []
valid_count = 0
total_minutes = 0

if not isinstance(records, list):
    print("输入错误，请提供列表")
else:
    for number, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            invalid.append(f"第 {number} 条必须是字典")
            continue
        if "title" not in record or "done" not in record or "minutes" not in record:
            invalid.append(f"第 {number} 条缺少字段")
            continue
        title = record["title"]
        done = record["done"]
        minutes = record["minutes"]
        if not isinstance(title, str) or not title.strip():
            invalid.append(f"第 {number} 条标题必须是非空字符串")
            continue
        if type(done) is not bool:
            invalid.append(f"第 {number} 条 done 必须是布尔值")
            continue
        # bool 是 int 的子类，用 type 避免把 True 当作一分钟。
        if type(minutes) is not int or minutes < 0:
            invalid.append(f"第 {number} 条 minutes 必须是非负整数")
            continue
        valid_count += 1
        total_minutes += minutes
        if done:
            completed += 1
        else:
            pending.append(title.strip())

    print(f"输入 {len(records)} 条，有效 {valid_count} 条，无效 {len(invalid)} 条")
    print(f"已完成 {completed} 项")
    print(f"未完成 {pending}")
    print(f"有效记录共 {total_minutes} 分钟")
    for message in invalid:
        print(message)
