"""教学数据。完成 TODO，答案见 exercises.md。"""
records = [
    {"title": "变量", "done": True, "minutes": 20},
    {"title": "循环", "done": False, "minutes": 15},
    {"title": "列表", "done": True, "minutes": 25},
]
long_tasks = []
completed_minutes = 0
for record in records:
    # TODO 把 minutes 大于等于 20 的标题加入 long_tasks
    # TODO 只累加已完成记录的 minutes
    pass
print(long_tasks)
print(completed_minutes)
