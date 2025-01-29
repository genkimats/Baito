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
SHIFT_FORMAT = config.get_shift_format()
TIME_BARRIER = config.get_time_barrier()

WEEKDAY_WAGE = config.get_weekday_wage()
WEEKEND_WAGE = config.get_weekend_wage()
TRANSIT_FEE = config.get_transit_fee()

class BaitoManage:
    @classmethod
    def initialize_csv(cls, date):
        try:
            if not date:
                csv_file = "worktime_info/" + FILE_FORMAT + get_current_date()
            else:
                csv_file = "worktime_info/" + FILE_FORMAT + date
            pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(csv_file, index=False)
        print("initialized.")

    @classmethod
    def add_entry(cls, year_month, day, start_time, end_time) -> int:
        cls.initialize_csv(year_month)
        date = year_month+"-"+day
        new_entry = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        }
        csv_file = "worktime_info/" + FILE_FORMAT + year_month
    
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
    def remove_entry(cls, year_month, day) -> bool:
        csv_file = "worktime_info/" + FILE_FORMAT + year_month
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
    def get_monthly_pay(cls, year_month) -> str:
        csv_file = "worktime_info/" + FILE_FORMAT + year_month
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

            if pd.to_datetime(row["end_time"], format=SHIFT_FORMAT).time() > datetime.strptime(TIME_BARRIER, SHIFT_FORMAT).time():
                before_ten = (datetime.strptime(TIME_BARRIER, SHIFT_FORMAT)
                              - pd.to_datetime(row["start_time"], format=SHIFT_FORMAT))
                after_ten = (pd.to_datetime(row["end_time"], format=SHIFT_FORMAT)
                             - datetime.strptime(TIME_BARRIER, SHIFT_FORMAT))
                before_ten_paying = int(before_ten.total_seconds())/(60**2) * base_wage
                after_ten_paying = int(int(after_ten.total_seconds())/(60**2) * base_wage * 1.25)
                daily_paying = before_ten_paying + after_ten_paying
                # print(str(before_ten.total_seconds() / (60 ** 2)))
                # print(str(after_ten.total_seconds() / (60 ** 2)))
            else:
                work_time = (pd.to_datetime(row["end_time"], format=SHIFT_FORMAT)
                             - pd.to_datetime(row["start_time"], format=SHIFT_FORMAT))
                daily_paying = work_time.total_seconds() * base_wage/(60**2)
            # print(thousands_separators(daily_paying))
            total_paying += daily_paying + (2*TRANSIT_FEE)
        formatted_total_paying = str(thousands_separators(int(total_paying)))
        print("\nTotal paying: " + formatted_total_paying + " yen")
        return formatted_total_paying
        