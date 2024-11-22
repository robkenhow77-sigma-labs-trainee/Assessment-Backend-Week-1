"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    # `DD.MM.YYYY`
    return datetime.strptime(date_val, "%d.%m.%Y")


def get_days_between(first: datetime, last: datetime) -> int:
    return (last - first).days
    


def get_day_of_week_on(date_val: datetime) -> str:
    return convert_to_datetime(date_val).strftime("%A")


def get_current_age(birthdate: date) -> int:
    print(date.now())

# a = convert_to_datetime("11.01.2001")
# b = convert_to_datetime("15.01.2001")
# print(get_days_between(a, b))
# print(get_day_of_week_on("21.11.2024"))
get_current_age(datetime.now())
