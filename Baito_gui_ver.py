#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from module.utils import get_current_date
from module.baito_configuration import BaitoConfiguration
from module.shift_manage import BaitoManage
from datetime import datetime, date
from time import sleep
config = BaitoConfiguration()

DATE_FORMAT = config.get_date_format()


def add_workday(root: tk.Tk, date: str, start_time: str, end_time: str) -> None:
  """
  Add a workday to the csv file.
  Called when the user clicks the "Add Workday" button or presses the Enter key.

  Args:
      root (tk.Tk): The root window.
      date (str): year, month, and day in "yyyy-mm-dd" format.
      start_time (str): start time in "hh:mm" format.
      end_time (str): end time in "hh:mm" format.
  """
  if date == "":
    messagebox.showerror("Error", "Please select a date")
    root.update_idletasks()
    return
  year, month, day = date.split("-")
  state = BaitoManage.add_entry(f"{year}-{month}", day, start_time, end_time)
  if state == 0:
    messagebox.showinfo("Success", "Entry added successfully")
  elif state == -1:
    messagebox.showerror("Error", "Invalid year/month or day")
  elif state == -2:
    messagebox.showerror("Error", "Entry with the same date already exists")
    
  root.update_idletasks()

def remove_workday(root: tk.Tk, date: str) -> None:
  """
  Remove a workday from the csv file.
  Called when the user clicks the "Delete Workday" button or presses the Enter key.

  Args:
      root (tk.Tk): The root window.
      date (str): year, month, and day in "yyyy-mm-dd" format.
  """
  if date == "":
    messagebox.showerror("Error", "Please select a date")
    root.update_idletasks()
    return
  year, month, day = date.split("-")
  state = BaitoManage.remove_entry(f"{year}-{month}", day)
  if state == 0:
    messagebox.showinfo("Success", "Entry removed successfully")
  elif state == -1:
    messagebox.showerror("Error", "Invalid year/month or day")
    
  root.update_idletasks()

def get_monthly_pay(root: tk.Tk, year: str, month: str) -> str:
  """
  Get the total pay for the month.
  Called when the user clicks the "Get Paying" button or presses the Enter key

  Args:
      root (tk.Tk): The root window.
      year (str): year in "yyyy" format.
      month (str): month in "mm" format.

  Returns:
      str: The total pay for the month.
  """
  try:
    total_pay = BaitoManage.get_monthly_pay(f"{year}-{month}", returntype="str")
    return f"{total_pay}"
  except:
    messagebox.showerror("Error", "Invalid year/month")
    root.update_idletasks()
    return "---"

def get_yearly_pay(root: tk.Tk, year: str) -> str:
  """
  Get the total pay for the year.
  Called when the user clicks the "Get Paying" button or presses the Enter key

  Args:
      root (tk.Tk): The root window.
      year (str): year in "yyyy" format.

  Returns:
      str: The total pay for the year.
  """
  total_pay = BaitoManage.get_yearly_pay(year, returntype="str")
  return f"{total_pay}"
  try:
    total_pay = BaitoManage.get_yearly_pay(root, year, returntype="str")
    return f"{total_pay}"
  except:
    messagebox.showerror("Error", "Invalid year")
    root.update_idletasks()
    return "---"

def get_workdays(root: tk.Tk, year: str, month: str) -> list[str]:
  """
  Get the workdays for the month.

  Args:
      root (tk.Tk): The root window.
      year (str): year in "yyyy" format.
      month (str): month in "mm" format.

  Returns:
      list[str]: The workdays for the month.
  """
  try:
    workdays = BaitoManage.get_workdays_list(f"{year}-{month}")
    return workdays
  except:
    messagebox.showerror("Error", "Invalid year/month")
    root.update_idletasks()
    return []


def setup_add_tab(root: tk.Tk, frame: tk.Frame) -> None:
  """
  Setup the "Add Workday" tab.

  Args:
      root (tk.Tk): The root window.
      frame (tk.Frame): The frame to add the widgets to.
  """
  year, month = list(map(lambda x: int(x), get_current_date().split("-")))
  cal = Calendar(frame, 
                 selectmode = 'day',
                 year = year, 
                 month = month,
                 showweeknumbers = False,
                 showothermonthdays = False,
                 date_pattern = 'yyyy-mm-dd',
                 font = ("Roman", 12, "bold"),
                 headerfont = ("Roman", 14, "bold"),
                 firstweekday = 'sunday',
                 background="white",
                 foreground="black",
                 headersforeground="black",
                 normalforeground="black",
                 weekendforeground="red",
                 selectforeground="blue")
  cal.pack(padx=10, pady=(20, 0), fill="both")
  workdays = get_workdays(root, str(year), f"{month:02d}")
  workdays_set = set()
  if workdays:
    workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)
    for day in workdays_set:
      try:
          cal.calevent_create(date(year, month, int(day)), 'Workday', 'workday')
      except ValueError:
          pass
    cal.tag_config('workday', background='grey', foreground='lightgrey')
  
  def on_month_change(event):
    cal.calevent_remove('nonworkday')
    new_month, new_year = cal.get_displayed_month()
    workdays = get_workdays(root, str(new_year), f"{new_month:02d}")
    if workdays:
      workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)

      for day in workdays_set:
          try:
              cal.calevent_create(date(new_year, new_month, day), 'Workday', 'workday')
          except ValueError:
              pass

  cal.bind("<<CalendarMonthChanged>>", on_month_change)
  
  def on_date_selected(event):
    selected_date = cal.get_date()
    selected_date_obj = datetime.strptime(selected_date, DATE_FORMAT).day
    new_month, new_year = cal.get_displayed_month()
    workdays = get_workdays(root, str(new_year), f"{new_month:02d}")
    if workdays:
      workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)
      if selected_date_obj in workdays_set:
          print("Selection disabled for:", selected_date)
          cal.selection_clear()

  cal.bind("<<CalendarSelected>>", on_date_selected)
  
  time_frame = tk.LabelFrame(frame, text="Working Hours", padx=10, pady=10)
  time_frame.pack(padx=10, pady=(0, 10), fill="x")
  
  minutes_tuple = tuple(range(0, 60, config.get_pay_interval_minutes()))
  minutes_tuple = tuple(map(lambda x: f"{x:02d}", minutes_tuple))
  
  start_time_frame = tk.Frame(time_frame)
  start_time_frame.grid(row=0, column=0)
  tk.Label(start_time_frame, text="Start Time:").grid(row=0, column=0, padx=5, pady=5)
  
  default_start_time = list(map(int, config.get_default_start_time().split(":")))
  start_hour = tk.IntVar(value=default_start_time[0])
  start_minute = tk.IntVar(value=default_start_time[1])
  
  start_hour_box = tk.Spinbox(start_time_frame, width=2, from_=0, to=23, textvariable=start_hour)
  start_hour_box.grid(row=0, column=1, padx=0, pady=5)
  
  tk.Label(start_time_frame, text=":").grid(row=0, column=2, padx=0, pady=5)
  
  start_minute_box = tk.Spinbox(start_time_frame, width=2, values=minutes_tuple, textvariable=start_minute, wrap=True)
  start_minute_box.grid(row=0, column=3, padx=0, pady=5)
  
  
  end_time_frame = tk.Frame(time_frame)
  end_time_frame.grid(row=1, column=0)
  tk.Label(end_time_frame, text="End Time:").grid(row=1, column=0, padx=(5, 11), pady=5)
  
  default_end_time = list(map(int, config.get_default_end_time().split(":")))
  end_hour = tk.IntVar(value=default_end_time[0])
  end_minute = tk.IntVar(value=default_end_time[1])
  
  end_hour_box = tk.Spinbox(end_time_frame, width=2, from_=0, to=23, textvariable=end_hour)
  end_hour_box.grid(row=1, column=1, padx=0, pady=5)
  
  tk.Label(end_time_frame, text=":").grid(row=1, column=2, padx=0, pady=5)
  
  end_minute_box = tk.Spinbox(end_time_frame, width=2, values=minutes_tuple, textvariable=end_minute, wrap=True)
  end_minute_box.grid(row=1, column=3, padx=0, pady=5)
  
  def reset_time():
    start_hour.set(f"{default_start_time[0]:02d}")
    start_minute.set(f"{default_start_time[1]:02d}")
    end_hour.set(f"{default_end_time[0]:02d}")
    end_minute.set(f"{default_end_time[1]:02d}")
  
  def on_enter(event=None):
    add_workday(root, cal.get_date(), f"{start_hour_box.get()}:{start_minute_box.get()}", f"{end_hour_box.get()}:{end_minute_box.get()}")
    cal.selection_clear()
    on_month_change(event)
    reset_time()
    
    
  tk.Button(frame,
            text="Add Workday",
            command=on_enter,
            font=("Arial", 14, "bold"),
            fg="black",
            bg="blue",
            activeforeground="green",
            activebackground="green",
            width=10,
            height=2,
            relief="ridge",
            bd=5
            ).pack(pady=(10, 0), ipadx=10, ipady=0)
  
  frame.bind('<Return>', lambda event: on_enter(event))  

def setup_delete_tab(root: tk.Tk, frame: tk.Frame) -> None:
  """
  Setup the "Delete Workday" tab.

  Args:
      root (tk.Tk): The root window.
      frame (tk.Frame): The frame to add the widgets to.
  """
  all_days = set(range(1, 32))
  year, month = list(map(lambda x: int(x), get_current_date().split("-")))
  cal = Calendar(frame, 
                 selectmode = 'day',
                 year = year, 
                 month = month,
                 showweeknumbers = False,
                 showothermonthdays = False,
                 date_pattern = 'yyyy-mm-dd',
                 font = ("Roman", 12, "bold"),
                 headerfont = ("Roman", 14, "bold"),
                 firstweekday = 'sunday',
                 background="white",
                 foreground="black",
                 headersforeground="black",
                 normalforeground="black",
                 weekendforeground="red",
                 selectforeground="blue")
  cal.pack(padx=10, pady=(20, 0), fill="both")
  
  workdays = get_workdays(root, str(year), f"{month:02d}")

  if workdays:
    workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)
    non_workdays = all_days - workdays_set

    for day in non_workdays:
        try:
            cal.calevent_create(date(year, month, day), 'NonWorkday', 'nonworkday')
        except ValueError:
            pass

    cal.tag_config('nonworkday', background='grey', foreground='lightgrey')
  
  def on_month_change(event):
    cal.calevent_remove('nonworkday')
    new_month, new_year = cal.get_displayed_month()
    workdays = get_workdays(root, str(new_year), f"{new_month:02d}")
    if workdays:
      workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)
      non_workdays = all_days - workdays_set
    else:
      non_workdays = all_days

    for day in non_workdays:
          try:
              cal.calevent_create(date(new_year, new_month, day), 'NonWorkday', 'nonworkday')
          except ValueError:
              pass

  cal.bind("<<CalendarMonthChanged>>", on_month_change)
  
  def on_date_selected(event):
    selected_date = cal.get_date()
    selected_date_obj = datetime.strptime(selected_date, DATE_FORMAT).day
    new_month, new_year = cal.get_displayed_month()
    workdays = get_workdays(root, str(new_year), f"{new_month:02d}")
    if workdays:
      workdays_set = set(datetime.strptime(day, DATE_FORMAT).day for day in workdays)
      non_workdays = all_days - workdays_set
      if selected_date_obj in non_workdays:
          print("Selection disabled for:", selected_date)
          cal.selection_clear()

  cal.bind("<<CalendarSelected>>", on_date_selected)
  
  def on_enter(event=None):
    remove_workday(root, cal.get_date())
    cal.selection_clear()
    on_month_change(event)
  
  tk.Button(frame,
            text="Delete Workday",
            command=on_enter,
            font=("Arial", 14, "bold"),
            fg="black",
            bg="blue",
            activeforeground="green",
            activebackground="green",
            width=10,
            height=2,
            relief="ridge",
            bd=5
            ).pack(pady=(10, 0), ipadx=10)
    
  frame.bind('<Return>', lambda event: on_enter(event))

def setup_paying_tab(root: tk.Tk, frame: tk.Frame) -> None:
  """
  Setup the "View Paying" tab.

  Args:
      root (tk.Tk): The root window.
      frame (tk.Frame): The frame to add the widgets to.
  """
  
  def setup_monthly_tab(root: tk.Tk, tab_monthly: tk.Frame) -> None:
    """
    Setup the "Monthly Pay" tab.

    Args:
        root (tk.Tk): The root window.
        tab_monthly (tk.Frame): The frame to add the widgets to.
    """
    
    date_frame = tk.LabelFrame(tab_monthly, text="Select Date", padx=10, pady=10)
    date_frame.pack(padx=10, pady=10, fill="x")
    
    #region columnconfig
    date_frame.grid_columnconfigure(0, weight=1)
    date_frame.grid_columnconfigure(1, weight=1)
    date_frame.grid_columnconfigure(2, weight=1)
    date_frame.grid_columnconfigure(3, weight=1)
    date_frame.grid_columnconfigure(4, weight=1)
    date_frame.grid_columnconfigure(5, weight=1)
    #endregion

    tk.Label(date_frame, text="Year:", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="e")
    year = tk.StringVar(value=default_year)
    year_box = tk.Spinbox(date_frame, 
                              from_=int(default_year) - 50,
                              to=int(default_year) + 50, 
                              textvariable=year,
                              wrap=True,font=("Arial", 14, "bold"), 
                              width=5)
    year_box.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="w")
    
    tk.Label(date_frame, text="Month:", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=(0, 0), pady=5, sticky="e")
    month = tk.StringVar(value=default_month)
    month_box = tk.Spinbox(date_frame, 
                              values=months_tuple,
                              textvariable=month,
                              wrap=True,
                              font=("Arial", 14, "bold"),
                              width=5)
    month_box.grid(row=0, column=4, padx=(5, 0), pady=5, sticky="w")
    month_box.delete(0, "end")
    month_box.insert(0, default_month)

    pay_frame = tk.LabelFrame(tab_monthly, text="Total Paying", padx=10, pady=10)
    pay_frame.pack(padx=10, pady=0, fill="x")

    #region columnconfig
    pay_frame.grid_columnconfigure(0, weight=1)
    pay_frame.grid_columnconfigure(1, weight=1)
    pay_frame.grid_columnconfigure(2, weight=1)
    pay_frame.grid_columnconfigure(3, weight=2)
    #endregion


    tk.Label(pay_frame, text="Total Paying", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    total_paying = tk.Label(pay_frame, text="---", font=("Arial", 14, "bold"))
    total_paying.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    def on_enter(event=None):
      total_paying.config(text=get_monthly_pay(root, year_box.get(), month_box.get()))
      
      
    tk.Button(tab_monthly,
              text="Get Paying",
              command=on_enter,
              font=("Arial", 14, "bold"),
              fg="black",
              bg="blue",
              activeforeground="green",
              activebackground="green",
              width=10,
              height=2,
              relief="ridge",
              bd=5
              ).pack(padx=5, pady=5)

    tab_monthly.bind('<Return>', on_enter)

  def setup_yearly_tab(root: tk.Tk, tab_yearly: tk.Frame) -> None:
    """
    Setup the "Yearly Pay" tab.

    Args:
        root (tk.Tk): The root window.
        tab_yearly (tk.Frame): The frame to add the widgets to.
    """
    date_frame = tk.LabelFrame(tab_yearly, text="Select Date", padx=10, pady=10)
    date_frame.pack(padx=10, pady=10, fill="x")
    
    #region columnconfig
    date_frame.grid_columnconfigure(0, weight=1)
    date_frame.grid_columnconfigure(1, weight=1)
    date_frame.grid_columnconfigure(2, weight=1)
    date_frame.grid_columnconfigure(3, weight=1)
    #endregion

    tk.Label(date_frame, text="Year:", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=0, pady=5, sticky="E")
    year = tk.StringVar(value=default_year)
    year_box = tk.Spinbox(date_frame,
                            from_=int(default_year) - 50,
                            to=int(default_year) + 50,
                            textvariable=year,
                            wrap=True,
                            font=("Arial", 14, "bold"),
                            width=5)
    year_box.grid(row=0, column=2, padx=(0, 0), pady=5, sticky="W")

    pay_frame = tk.LabelFrame(tab_yearly, text="Total Paying", padx=10, pady=10)
    pay_frame.pack(padx=10, pady=0, fill="x")

    #region columnconfig
    pay_frame.grid_columnconfigure(0, weight=1)
    pay_frame.grid_columnconfigure(1, weight=1)
    pay_frame.grid_columnconfigure(2, weight=1)
    pay_frame.grid_columnconfigure(3, weight=2)
    #endregion

    def on_enter(event=None):
      total_paying.config(text=get_yearly_pay(root, year_box.get()))

    tk.Label(pay_frame, text="Total Paying", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    total_paying = tk.Label(pay_frame, text="---", font=("Arial", 14, "bold"))
    total_paying.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    tk.Button(tab_yearly,
              text="Get Paying",
              command=on_enter,
              font=("Arial", 14, "bold"),
              fg="black",
              bg="blue",
              activeforeground="green",
              activebackground="green",
              width=10,
              height=2,
              relief="ridge",
              bd=5
              ).pack(padx=5, pady=5)
      
    tab_yearly.bind('<Return>', on_enter)
  
  default_year, default_month = get_current_date().split("-")
  months_tuple = tuple(range(1, 13))
  months_tuple = tuple(map(lambda x: f"{x:02d}", months_tuple))
  
  notebook_paying = ttk.Notebook(frame)
  notebook_paying.pack(expand=True, fill='both')

  tab_monthly = ttk.Frame(notebook_paying)
  tab_yearly = ttk.Frame(notebook_paying)

  notebook_paying.add(tab_monthly, text='Monthly Pay')
  notebook_paying.add(tab_yearly, text='Yearly Pay')
  
  setup_monthly_tab(root, tab_monthly)
  setup_yearly_tab(root, tab_yearly)
  
  def on_tab_change(event):
    if notebook_paying.index("current") == 0:
      tab_monthly.focus_set()
    else:
      tab_yearly.focus_set()
  root.slaves()[0].bind("<<NotebookTabChanged>>", on_tab_change)
  
  

def main():
  root = tk.Tk()
  root.title(u"Baito")
  root.geometry("450x450")
  root.resizable(False, False)

  notebook = ttk.Notebook(root)
  notebook.pack(expand=True, fill='both')

  tab_add = ttk.Frame(notebook)
  tab_delete = ttk.Frame(notebook)
  tab_paying = ttk.Frame(notebook)

  notebook.add(tab_add, text='Add Workday')
  notebook.add(tab_delete, text='Delete Workday')
  notebook.add(tab_paying, text='View Paying')

  setup_add_tab(root, tab_add)
  setup_delete_tab(root, tab_delete)
  setup_paying_tab(root, tab_paying)
  
  tab_add.focus_set()
  
  
  while True:
      try:
        root.update_idletasks()
        root.update()
        print(root.focus_get())
      except tk.TclError:
        break
      sleep(1)

  root.mainloop()

if __name__ == "__main__":
  main()
