def is_leap_year(year):
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def next_date(year, month, day):
    """计算下一天的日期"""
    # 每月的天数（非闰年）
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # 处理闰年2月的情况
    if is_leap_year(year):
        days_in_month[1] = 29
    
    # 检查输入日期是否有效
    if not (1 <= month <= 12):
        raise ValueError("月份必须在1-12之间")
    if not (1 <= day <= days_in_month[month - 1]):
        raise ValueError(f"{month}月没有{day}日")
    
    # 计算下一天
    day += 1
    if day > days_in_month[month - 1]:
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    return year, month, day

# 测试用例
test_cases = [
    (2023, 1, 1),      # 普通情况
    (2023, 12, 31),    # 年末
    (2024, 2, 28),     # 闰年2月
    (2023, 2, 28),     # 非闰年2月
    (2024, 12, 31),    # 闰年跨年
    (2023, 4, 30),     # 小月月底
]

for y, m, d in test_cases:
    try:
        next_y, next_m, next_d = next_date(y, m, d)
        print(f"{y}-{m}-{d} 的下一天是: {next_y}-{next_m}-{next_d}")
    except ValueError as e:
        print(f"输入错误: {e}")    