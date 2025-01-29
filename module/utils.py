from datetime import datetime
from module.baito_configuration import BaitoConfiguration

config = BaitoConfiguration()
FILE_DATE_FORMAT = config.get_file_date_format()


def thousands_separators(num):
    return '{:,}'.format(num)

def get_current_date():
    return datetime.today().strftime(FILE_DATE_FORMAT)