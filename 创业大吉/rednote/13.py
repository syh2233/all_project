def is_good_date(start_year, end_year):
    count = 0
    start_day = 1  # 1901年1月1日是星期二
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if month in [1, 3, 5, 7, 8, 10, 12]:  # 大月
                days = 31
            elif month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    days = 29  # 闰年
                else:
                    days = 28  # 平年
            else:  # 小月
                days = 30

            for day in [1, 11, 21, 31]:
                if day <= days:
                    # 计算星期，起始星期为星期二（1）
                    weekday = (start_day + (365 * (year - 1901) + sum(
                        [31, 28 + is_leap(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]) - 1)) % 7
                    if weekday == 0:  # 星期一
                        count += 1
    return count


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# 计算从1901年1月1日至2024年12月31日的一好日期总数
good_dates_count = is_good_date(1901, 2024)
print(good_dates_count)