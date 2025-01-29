from datetime import datetime
from module.baito_configuration import BaitoConfiguration


config = BaitoConfiguration()

csv_file = None
FILE_FORMAT = config.get_file_format()
COLUMNS = config.get_columns()
FILE_DATE_FORMAT = config.get_file_date_format()
DATE_FORMAT = config.get_date_format()
SHIFT_FORMAT = config.get_shift_format()
TIME_BARRIER = config.get_time_barrier()


def get_year_month(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%Y-%m")

    try:
        valid_date = datetime.strptime(date_str, "%Y-%m")
        return valid_date.strftime("%Y-%m")
    except ValueError:
        print("Invalid date format. Please enter the date in yyyy-mm-dd format.")
        return get_year_month(prompt, allow_default)


def get_day(prompt, allow_default=False):
    day_str = input(prompt)
    if allow_default and not day_str:
        return datetime.today().strftime("%d")

    try:
        valid_date = datetime.strptime(day_str, "%d")
        return valid_date.strftime("%d")
    except ValueError:
        print("Invalid date format. Please enter the date in yyyy-mm-dd format.")
        return get_day(prompt, allow_default)


def get_start_time(prompt, allow_default=False):
    start_time = input(prompt)
    if allow_default and not start_time:
        return "17:00"

    try:
        valid_date = datetime.strptime(start_time, SHIFT_FORMAT)
        return start_time
    except ValueError:
        print("Invalid time format. Please enter the date in HH:MM format.")
        return get_start_time(prompt, allow_default)


def get_end_time(prompt):
    end_time = input(prompt)
    try:
        valid_date = datetime.strptime(end_time, SHIFT_FORMAT)
        return end_time
    except ValueError:
        print("Invalid time format. Please enter the date in HH:MM format.")
        return get_end_time(prompt)