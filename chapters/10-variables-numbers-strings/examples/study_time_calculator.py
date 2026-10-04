def calculate_study_time(study_days, minutes_per_day):
    total_minutes = study_days * minutes_per_day
    full_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    decimal_hours = total_minutes / 60
    return total_minutes, full_hours, remaining_minutes, decimal_hours


def main():
    topic = input("学习主题：").strip()
    study_days = int(input("计划学习几天："))
    minutes_per_day = int(input("每天学习多少分钟："))

    total_minutes, full_hours, remaining_minutes, decimal_hours = (
        calculate_study_time(study_days, minutes_per_day)
    )

    print()
    print(f"主题：{topic}")
    print(f"总时长：{total_minutes} 分钟")
    print(f"换算结果：{full_hours} 小时 {remaining_minutes} 分钟")
    print(f"小数形式：{decimal_hours:.2f} 小时")


if __name__ == "__main__":
    main()
