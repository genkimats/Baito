"""
Module for utility functions that are used in the project.
"""
from datetime import datetime
from module.baito_configuration import BaitoConfiguration

config = BaitoConfiguration()
FILE_DATE_FORMAT = config.get_file_date_format()


def thousands_separators(num: int) -> str:
    """
    Add thousands separators to a number.

    Args:
        num (int): The number to add separators to (Salary) 

    Returns:
        str: The number with thousands separators.
    """
    return '{:,}'.format(num)

def get_current_date() -> str:
    """
    Get the current date in the format specified in the configuration file.

    Returns:
        str: The current date in the format specified in the configuration file.
    """
    return datetime.today().strftime(FILE_DATE_FORMAT)