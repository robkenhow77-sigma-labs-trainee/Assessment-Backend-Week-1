"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    # `DD.MM.YYYY`
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except:
        raise ValueError("Unable to convert value to datetime.")



def get_days_between(first: datetime, last: datetime) -> int:
    try:
        return (last - first).days
    except:
        raise TypeError("Datetimes required.")
    


def get_day_of_week_on(date_val: datetime) -> str:
    try:
        if isinstance(date_val, datetime):
            
        return convert_to_datetime(date_val).strftime("%A")
    except:
        raise TypeError("Datetime required.")


def get_current_age(birthdate: date) -> int:
    try:
        current_time = datetime.now().date()
        same_year = date(current_time.year, birthdate.month, birthdate.day)
        if same_year >= current_time:
            return current_time.year - birthdate.year - 1
        return current_time.year - birthdate.year
    except:
        raise TypeError("Date required.")

