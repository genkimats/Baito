from datetime import datetime
from module.shift_manage import BaitoManage, get_year_month, get_day, get_start_time, get_end_time
from module.baito_configuration import BaitoConfiguration

config = BaitoConfiguration()

FILE_FORMAT = config.get_file_format()
COLUMNS = config.get_columns()
FILE_DATE_FORMAT = config.get_file_date_format()
DATE_FORMAT = config.get_date_format()
SHIFT_FORMAT = config.get_shift_format()
TIME_BARRIER = config.get_time_barrier()

WEEKDAY_WAGE = config.get_weekday_wage()
WEEKEND_WAGE = config.get_weekend_wage()
TRANSIT_FEE = config.get_transit_fee()

def add():
    year_month = get_year_month("Enter year & month of work in the format yyyy-mm or blank for current month: ",
                                allow_default=True)
    day = get_day("Enter day of work in format dd or blank for today: ", allow_default=True)
    start_time = get_start_time("Enter starting time in the format HH:MM or blank for 17:00: ",
                                allow_default=True)
    end_time = get_end_time("Enter ending time in the format HH:MM: ")
    BaitoManage.add_entry(year_month, day, start_time, end_time)


def remove():
    year_month = get_year_month("Enter year & month of work in the format yyyy-mm or blank for current month: ",
                                allow_default=True)
    day = get_day("Enter day of work in format dd or blank for today: ", allow_default=True)
    BaitoManage.remove_entry(year_month, day)
    
def monthly_pay():
    year_month = input("Enter desired date of viewing (yyyy-mm) or blank for current month: ")
    if not year_month:
        year_month = datetime.today().strftime(BaitoManage.FILE_DATE_FORMAT)
    valid = False
    fail_count = 0
    while not valid:
        if BaitoManage.get_monthly_pay(year_month):
            valid = True
        else:
            fail_count += 1
            if fail_count > 5:
                print("\nToo many tries. Re-run the program again.")
                quit()
            year_month = get_year_month("Re-enter year & month of work in the format yyyy-mm or blank for current month: ",
                                    allow_default=True)
    

def main():
    while True:
        print("1. Add new work day.\n"
              "2. Remove work day.\n"
              "3. View total paying.\n"
              "4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == "1":
            add()
        elif choice == "2":
            remove()
        elif choice == "3":
            monthly_pay()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Choose from 1-4.")
        print("\n")


if __name__ == "__main__":
    main()
