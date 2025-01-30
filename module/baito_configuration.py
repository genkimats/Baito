"""
Module for reading the configuration file and returning the values of the configuration.
"""
from dotenv import load_dotenv
import os

class BaitoConfiguration:
    def __init__(self):
        config_path = "baito_config.env"
        load_dotenv(config_path)
    
    def get_weekday_wage(self) -> int:
        return int(os.getenv("WEEKDAY_WAGE"))
    
    def get_weekend_wage(self) -> int:
        return int(os.getenv("WEEKEND_WAGE"))
    
    def get_transit_fee(self) -> int:
        return int(os.getenv("TRANSIT_FEE"))
    
    def get_pay_interval_minutes(self) -> int:
        return int(os.getenv("PAY_INTERVAL_MINUTES"))
    
    def get_default_start_time(self) -> str:
        return os.getenv("DEFAULT_START_TIME")
    
    def get_default_end_time(self) -> str:
        return os.getenv("DEFAULT_END_TIME")
    
    def get_time_barrier(self) -> str:
        return os.getenv("TIME_BARRIER")
    
    def get_file_format(self) -> str:
        return os.getenv("FILE_FORMAT")
    
    def get_columns(self) -> list:
        return str(os.getenv("COLUMNS")).split(",")
    
    def get_file_date_format(self) -> str:
        return os.getenv("FILE_DATE_FORMAT")
    
    def get_date_format(self) -> str:
        return os.getenv("DATE_FORMAT")
    
    def get_shift_format(self) -> str:
        return os.getenv("SHIFT_FORMAT")