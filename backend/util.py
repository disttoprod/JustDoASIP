from datetime import date, datetime
from dateutil.parser import parse

import pandas as pd

DATE = str | date | datetime
FORMAT = "%Y-%m-%d"


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


if __name__ == "__main__":
    print(get_normalized_date("20240501"))
    print(get_normalized_date("2024-05-01"))
    print(get_normalized_date("2024-05-01 00:00"))
    print(get_normalized_date(get_date("2024-05-01")))
    print(get_normalized_date(get_date("2024-05-01 00:00")))

    print(get_months_between("2021-01-05", "2024-07-05"))
