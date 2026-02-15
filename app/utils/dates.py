"""
Date utility functions - COMPLETE
"""

from datetime import datetime, timedelta, date

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_date(date_string):
    """Parse date string - handles date, datetime, and string formats."""
    
    if not date_string:
        return datetime.now().date()

    # If already a date object
    if isinstance(date_string, date) and not isinstance(date_string, datetime):
        return date_string

    # If already a datetime object
    if isinstance(date_string, datetime):
        return date_string.date()

    # If it's a string, try parsing
    if isinstance(date_string, str):
        for fmt in (DATETIME_FORMAT, DATE_FORMAT):
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue

        try:
            return datetime.strptime(date_string.split()[0], DATE_FORMAT).date()
        except (ValueError, IndexError):
            pass

    # Fallback
    return datetime.now().date()


def format_date(date_obj):
    """Format date object to string"""
    return date_obj.strftime(DATE_FORMAT)


def get_today():
    """Get today's date"""
    return datetime.now().date()


def get_yesterday():
    """Get yesterday's date"""
    return datetime.now().date() - timedelta(days=1)


def get_date_string(date_obj=None):
    """Get date string (default: today)"""
    if date_obj is None:
        date_obj = get_today()
    return format_date(date_obj)


def days_between(date1, date2):
    """Calculate days between two dates"""
    return abs((date2 - date1).days)


def add_days(date_obj, days):
    """Add days to a date"""
    return date_obj + timedelta(days=days)


def subtract_days(date_obj, days):
    """Subtract days from a date"""
    return date_obj - timedelta(days=days)
