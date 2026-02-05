"""
Date utility functions
"""

from datetime import datetime, date, timedelta
from app.utils.constants import DATE_FORMAT


def get_today() -> str:
    """Get today's date as string in YYYY-MM-DD format"""
    return date.today().strftime(DATE_FORMAT)


def get_date_string(date_obj: date) -> str:
    """Convert date object to string"""
    return date_obj.strftime(DATE_FORMAT)


def parse_date(date_string: str) -> date:
    """Parse date string to date object"""
    return datetime.strptime(date_string, DATE_FORMAT).date()


def get_days_between(date1: str, date2: str) -> int:
    """Get number of days between two dates"""
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    return abs((d2 - d1).days)


def get_yesterday() -> str:
    """Get yesterday's date as string"""
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime(DATE_FORMAT)


def is_today(date_string: str) -> bool:
    """Check if given date string is today"""
    return date_string == get_today()
