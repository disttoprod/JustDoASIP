from datetime import date, datetime
from dateutil.parser import parse
import math

import pandas as pd

DATE = str | date | datetime
FORMAT = "%Y-%m-%d"

################################ DATE UTILS ####################################


def get_date(_date: DATE) -> date:
    if isinstance(_date, str):
        _date = parse(_date)

    if isinstance(_date, datetime):
        return _date.date()
    elif isinstance(_date, date):
        return _date
    else:
        raise NotImplementedError


def get_normalized_date(_date: DATE) -> str:
    _date = get_date(_date)
    return _date.strftime(FORMAT)


def get_months_between(start: DATE, end: DATE) -> list[str]:
    """
    Return a list of month *ends* between `start` and `end` in the `FORMAT`.
    """
    start, end = get_date(start), get_date(end)
    return pd.date_range(start, end, freq="ME").strftime(FORMAT).tolist()


################################################################################


def format_money(money: int) -> str:
    """
    Only works for Indian currency right now.
    """
    power_of_ten = int(math.log10(money)) if money > 0 else 0
    short_money = money
    char = ""
    match power_of_ten:
        case 0 | 1 | 2:
            pass
        case 3 | 4:
            short_money = money / (10**3)
            char = "K"
        case 5 | 6:
            short_money = money / (10**5)
            char = "L"
        case _:
            short_money = money / (10**7)
            char = "Cr"

    str_money = f"{short_money:.2f}{char}"
    return str_money


if __name__ == "__main__":
    print(get_normalized_date("20240501"))
    print(get_normalized_date("2024-05-01"))
    print(get_normalized_date("2024-05-01 00:00"))
    print(get_normalized_date(get_date("2024-05-01")))
    print(get_normalized_date(get_date("2024-05-01 00:00")))
    print(get_months_between("2021-01-05", "2024-07-05"))

    print(format_money(2.4))
    print(format_money(24))
    print(format_money(240))
    print(format_money(2400))
    print(format_money(24000))
    print(format_money(240000))
    print(format_money(2400000))
    print(format_money(24000000))
