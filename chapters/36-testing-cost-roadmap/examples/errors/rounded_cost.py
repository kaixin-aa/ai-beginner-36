from decimal import Decimal
estimate=Decimal('0.004')
display=f'{estimate:.2f}'
print('错误显示',display)
assert Decimal(display)>0,'两位小数丢掉了小额估算，不能记录成实际0元'
