"""
date_utils.py
Utility functions for date parsing, formatting, and validation.
Uses ISO 8601 format (YYYY-MM-DD) for consistency.
"""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

def get_today_str() -> str:
    """
    Return today's date as a string in ISO format.

    Returns:
        str: Today's date in format 'YYYY-MM-DD'
        
    Example:
        >>> get_today_str()
        '2023-10-15'
    """
    return datetime.now().strftime(DATE_FORMAT)

def parse_date(date_str: str) -> datetime:
    """
    Convert a date string into a datetime object.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If date string is in wrong format
        
    Example:
        >>> parse_date("2023-10-15")
        datetime.datetime(2023, 10, 15, 0, 0)
    """
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError as e:
        raise ValueError(
            f"Invalid date format: '{date_str}'. Expected {DATE_FORMAT} (YYYY-MM-DD)"
        ) from e

def format_date(date_obj: datetime) -> str:
    """
    Convert a datetime object to ISO format string.

    Args:
        date_obj (datetime): The date to format
        
    Returns:
        str: Formatted date string
        
    Example:
        >>> format_date(2023, 10, 15)
        '2023-10-15'
    """
    return date_obj.strftime(DATE_FORMAT)

def days_between(start_date: str, end_date: str) -> int:
    """
    Calculate number of days between two date strings.

    Args:
        start_date (str): Start date in YYYY-MM-DD
        end_date (str): End date in YYYY-MM-DD
        
    Returns:
        int: Number of days between dates
        
    Example:
        >>> days_between("2023-10-01", "2023-10-15")
        14
    """
    start = parse_date(start_date)
    end = parse_date(end_date)
    return (end - start).days