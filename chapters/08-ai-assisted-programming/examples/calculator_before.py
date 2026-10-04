def calculate(left, operator, right):
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    raise ValueError("不支持的运算符")


if __name__ == "__main__":
    print(calculate(8, "+", 2))
