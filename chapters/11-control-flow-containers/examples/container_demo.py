"""配合正文运行，数据均为教学样例。"""
minutes = 35
if minutes >= 30:
    print("今天达标")
else:
    print("再学一会儿")
print(minutes >= 30 and minutes < 60)
print(not False)

topics = ["变量", "循环", "列表", "字典"]
print(topics[0])
print(topics[-1])
print(topics[1:3])
print(topics[10:])
topics.append("集合")
topics[0] = "变量复习"
for number, topic in enumerate(topics, start=1):
    print(number, topic)

total = 0
for minutes in [20, 15, 25]:
    total += minutes
print("总分钟数", total)
for number in range(1, 4):
    print("复习轮次", number)

remaining = 3
while remaining > 0:
    print("剩余次数", remaining)
    remaining -= 1
print("停止")

point = (2, 5)
x, y = point
print("坐标", x, y)
tags = {"Python", "AI", "Python"}
print("标签数", len(tags))
print("包含 AI", "AI" in tags)
print("空集合长度", len(set()))
record = {"title": "列表", "done": False}
print("标题", record["title"])
print("缺省分钟数", record.get("minutes", 0))
for key, value in record.items():
    print(key, value)
print("字符串 False 的真假", bool("False"))
