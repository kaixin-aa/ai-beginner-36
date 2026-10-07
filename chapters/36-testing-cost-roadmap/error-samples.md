# 第36章错误示例与修复

两个错误均为明确教学演示，不涉及新增API请求。错误文件实际退出1，修复版本退出0，详见[机器验证记录](./results/verification-summary.json)。

## 小额费用被显示为0

`examples/errors/rounded_cost.py`把教学估算0.004元格式化为两位小数，显示0.00，随后断言失败。这会让读者误以为费用为0。

`examples/fixed/rounded_cost.py`保留六位小数，并输出“教学估算费用 0.004000 元，非实际扣款”。计算值与展示值分别处理，避免将格式化结果当作真实账单。

## 离线核对被重复统计

`examples/errors/double_count.py`将真实5080与第34章原用量4535再次相加，得到9615，随后断言失败。

`examples/fixed/double_count.py`只统计两个原始真实调用来源，输出“真实请求 7 Token 5080”。离线核对和回放引用历史响应，不增加实际请求数。
