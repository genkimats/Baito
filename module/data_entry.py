"""
Module for getting user input for the data entry process.
Mainly used for the command line interface.
"""
from datetime import datetime
from module.baito_configuration import BaitoConfiguration


config = BaitoConfiguration()

csv_file = None
FILE_FORMAT = config.get_file_format()
COLUMNS = config.get_columns()
FILE_DATE_FORMAT = config.get_file_date_format()
DATE_FORMAT = config.get_date_format()
TIME_FORMAT = config.get_time_format()
TIME_BARRIER = config.get_time_barrier()


def get_year_month(prompt: str, allow_default: bool = False) -> str:
    """
    Get the year and month in "yyyy-mm" format from user input.

    Args:
        prompt (str): The prompt to show the user.
        allow_default (bool, optional): If True, allows the user to enter the input as blank. Defaults to False.

    Returns:
        str: The year and month in "yyyy-mm" format.
    """
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%Y-%m")

    try:
        valid_date = datetime.strptime(date_str, "%Y-%m")
        return valid_date.strftime("%Y-%m")
    except ValueError:
        print("Invalid date format. Please enter the date in yyyy-mm-dd format.")
        return get_year_month(prompt, allow_default)


def get_day(prompt: str, allow_default: bool = False) -> str:
    """
    Get the day in "dd" format from user input.

    Args:
        prompt (str): The prompt to show the user.
        allow_default (bool, optional): If True, allows the user to enter the input as blank. Defaults to False.

    Returns:
        str: The day in "dd" format.
    """
    day_str = input(prompt)
    if allow_default and not day_str:
        return datetime.today().strftime("%d")

    try:
        valid_date = datetime.strptime(day_str, "%d")
        return valid_date.strftime("%d")
    except ValueError:
        print("Invalid date format. Please enter the date in yyyy-mm-dd format.")
        return get_day(prompt, allow_default)


def get_start_time(prompt: str, allow_default: bool = False) -> str:
    """
    Get the start time in "HH:MM" format from user input.

    Args:
        prompt (str): The prompt to show the user.
        allow_default (bool, optional): If True, allows the user to enter the input as blank. Defaults to False.

    Returns:
        str: The start time in "HH:MM" format.
    """
    start_time = input(prompt)
    if allow_default and not start_time:
        return "17:00"

    try:
        valid_date = datetime.strptime(start_time, TIME_FORMAT)
        return start_time
    except ValueError:
        print("Invalid time format. Please enter the date in HH:MM format.")
        return get_start_time(prompt, allow_default)


def get_end_time(prompt: str) -> str:
    """
    Get the end time in "HH:MM" format from user input.

    Args:
        prompt (str): The prompt to show the user.

    Returns:
        str: The end time in "HH:MM" format.
    """
    end_time = input(prompt)
    try:
        valid_date = datetime.strptime(end_time, TIME_FORMAT)
        return end_time
    except ValueError:
        print("Invalid time format. Please enter the date in HH:MM format.")
        return get_end_time(prompt)