"""
Module for managing worktime data by directly interacting with the csv files.
It provides functions to add, remove, and calculate total paying for worktime entries.
"""
from datetime import datetime
import pandas as pd
import csv
from module.data_entry import get_year_month, get_day, get_start_time, get_end_time
from module.baito_configuration import BaitoConfiguration
from module.utils import get_current_date, thousands_separators

config = BaitoConfiguration()

csv_file = None
FILE_FORMAT = config.get_file_format()
COLUMNS = config.get_columns()
FILE_DATE_FORMAT = config.get_file_date_format()
DATE_FORMAT = config.get_date_format()
TIME_FORMAT = config.get_time_format()
TIME_BARRIER = config.get_time_barrier()

WEEKDAY_WAGE = config.get_weekday_wage()
WEEKEND_WAGE = config.get_weekend_wage()
TRANSIT_FEE = config.get_transit_fee()

class BaitoManage:
    @classmethod
    def initialize_csv(cls, year_month: str) -> None:
        """
        Initialize the csv file for worktime management.
        Can be called without checking if the file already exists.

        Args:
            year_month (str): year and month in "yyyy-mm" format.
        """
        try:
            if not year_month:
                csv_file = f"worktime_info/{FILE_FORMAT}{get_current_date()}.csv"
            else:
                csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
            pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(csv_file, index=False)
        print("initialized.")

    @classmethod
    def add_entry(cls, year_month: str, day: str, start_time: str, end_time: str) -> int:
        """
        Add an entry to the worktime csv file.

        Args:
            year_month (str): year and month in "yyyy-mm" format.
            day (str): day in "dd" format.
            start_time (str): start time in "hh:mm" format.
            end_time (str): end time in "hh:mm" format.

        Returns:
            int: 0 if successful, -1 if invalid year/month or day, -2 if entry with the same date already exists. -3 if invalid start/end time.
        """
        cls.initialize_csv(year_month)
        date = f"{year_month}-{day}"
        if start_time.split(":")[0] > end_time.split(":")[0] and start_time.split(":")[1] >= end_time.split(":")[1]:
            print("\nInvalid start/end time.")
            return -3
        
        start_time = f"{int(start_time.split(':')[0]):02d}:{int(start_time.split(':')[1]):02d}"
        end_time = f"{int(end_time.split(':')[0]):02d}:{int(end_time.split(':')[1]):02d}"
            
        new_entry = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        }
        csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
    
        try:
            df = pd.read_csv(csv_file)
            if date in df['date'].values:
                print("\nEntry with the same date already exists.")
                return -2
            with open(csv_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
                writer.writerow(new_entry)
                print(f"\n{date}  {start_time} - {end_time}\nEntry added successfully")
            return 0
        except:
            print("\nInvalid year/month or day.")
            return -1
        

    @classmethod
    def remove_entry(cls, year_month: str, day: str) -> int:
        """
        Remove an entry from the worktime csv file.

        Args:
            year_month (str): year and month in "yyyy-mm" format.
            day (str): day in "dd" format.

        Returns:
            int: 0 if successful, -1 if invalid year/month or day.
        """
        csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
        try:
            pd.read_csv(csv_file)
            with open(csv_file, "a", newline="") as csvfile:
                df_remove = pd.read_csv(csv_file)
                df_remove.set_index("date", inplace=True)
                date = f"{year_month}-{day}"
                removed = df_remove.drop(date)
                print(removed)
                removed.to_csv(csv_file, index=True)
                print("\nEntry successfully removed.")
                return 0
        except KeyError or FileNotFoundError:
            print("\nInvalid year/month or day.")
            return -1

    @classmethod
    def get_monthly_pay(cls, year_month: str, returntype: str = "int") -> int | str:
        """
        Calculate total paying for the queried month.

        Args:
            year_month (str): year and month in "yyyy-mm" format.
            returntype (str, optional): data type of return value ("str" or "int"). Defaults to "int".

        Returns:
            int | str: total paying for the queried month.
        """
        cls.initialize_csv(year_month)
        csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
        try:
            df = pd.read_csv(csv_file, names=COLUMNS, header=0)
        except FileNotFoundError:
            print("Invalid date or filename.")
            return None

        total_paying = 0
        for i, row in df.iterrows():
            if pd.to_datetime(row["date"], format=DATE_FORMAT).weekday() != 5:
                base_wage = WEEKDAY_WAGE
            else:
                base_wage = WEEKEND_WAGE

            if pd.to_datetime(row["end_time"], format=TIME_FORMAT).time() > datetime.strptime(TIME_BARRIER, TIME_FORMAT).time():
                before_ten = (datetime.strptime(TIME_BARRIER, TIME_FORMAT)
                              - pd.to_datetime(row["start_time"], format=TIME_FORMAT))
                after_ten = (pd.to_datetime(row["end_time"], format=TIME_FORMAT)
                             - datetime.strptime(TIME_BARRIER, TIME_FORMAT))
                before_ten_paying = int(before_ten.total_seconds())/(60**2) * base_wage
                after_ten_paying = int(int(after_ten.total_seconds())/(60**2) * base_wage * 1.25)
                daily_paying = before_ten_paying + after_ten_paying
                # print(str(before_ten.total_seconds() / (60 ** 2)))
                # print(str(after_ten.total_seconds() / (60 ** 2)))
            else:
                work_time = (pd.to_datetime(row["end_time"], format=TIME_FORMAT)
                             - pd.to_datetime(row["start_time"], format=TIME_FORMAT))
                daily_paying = work_time.total_seconds() * base_wage/(60**2)
            # print(thousands_separators(daily_paying))
            total_paying += daily_paying + (2*TRANSIT_FEE)
        formatted_total_paying = str(thousands_separators(int(total_paying)))
        print(f"\nTotal paying: {formatted_total_paying} yen")
        if returntype == "int":
            return total_paying
        elif returntype == "str":
            return formatted_total_paying
    
    @classmethod
    def get_yearly_pay(cls, year: str, returntype: str = "int") -> int | str:
        """
        Calculate total paying for the queried year.

        Args:
            year (str): year in "yyyy" format.
            returntype (str): data type of return value ("str" or "int"). Defaults to "int".

        Returns:
            int | str: total paying for the queried year.
        """
        total_paying = 0
        for month in range(1, 13):
            year_month = f"{year}-{month:02d}"
            monthly_paying = cls.get_monthly_pay(year_month, returntype="int")
            if monthly_paying:
                total_paying += monthly_paying
        formatted_total_paying = str(thousands_separators(int(total_paying)))
        print(f"\nTotal paying for {year}: {formatted_total_paying} yen")
        if returntype == "int":
            return total_paying
        elif returntype == "str":
            return formatted_total_paying
    
    @classmethod
    def get_workdays_list(cls, year: str, month: str) -> list[str]:
        """
        Get the list of workdays in the queried month.

        Args:
            year (str): year in "yyyy" format.
            month (str): month in "mm" format.

        Returns:
            list[str]: list of workdays in the queried month.
        """
        year_month = f"{year}-{month}"
        cls.initialize_csv(year_month)
        csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
        try:
            df = pd.read_csv(csv_file, names=COLUMNS, header=0)
        except FileNotFoundError:
            print("Invalid date or filename.")
            return None

        workdays = df["date"].tolist()
        return workdays
    
    @classmethod
    def get_workhours_list(cls, year: str, month: str) -> list[tuple[str, str]]:
        """
        Get the list of workhours in the queried month.

        Args:
            year (str): year in "yyyy" format.
            month (str): month in "mm" format.

        Returns:
            list[tuple[str, str]]: list of workhours in the queried month. e.g. [("hh:mm", "hh:mm"), ...]
        """
        year_month = f"{year}-{int(month):02d}"
        cls.initialize_csv(year_month)
        csv_file = f"worktime_info/{FILE_FORMAT}{year_month}.csv"
        try:
            df = pd.read_csv(csv_file, names=COLUMNS, header=0)
        except FileNotFoundError:
            print("Invalid date or filename.")
            return None

        workhours = []
        for _, row in df.iterrows():
            work_time = (row["start_time"], row["end_time"])
            workhours.append(work_time)
        return workhours
