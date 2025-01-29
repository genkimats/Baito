#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from module.utils import get_current_date
from module.baito_configuration import BaitoConfiguration
from module.shift_manage import BaitoManage

config = BaitoConfiguration()

#
# ボタンが押されるとここが呼び出される
#

def add_workday(date, start_time, end_time):
  year, month, day = date.split("-")
  state = BaitoManage.add_entry(f"{year}-{month}", day, start_time, end_time)
  if state == 0:
    messagebox.showinfo("Success", "Entry added successfully")
  elif state == -1:
    messagebox.showerror("Error", "Invalid year/month or day")
  elif state == -2:
    messagebox.showerror("Error", "Entry with the same date already exists")

def remove_workday(date):
  year, month, day = date.split("-")
  state = BaitoManage.remove_entry(f"{year}-{month}", day)
  if state == 0:
    messagebox.showinfo("Success", "Entry removed successfully")
  elif state == -1:
    messagebox.showerror("Error", "Invalid year/month or day")

def get_monthly_pay(year, month):
  try:
    total_pay = BaitoManage.get_monthly_pay(f"{year}-{month}")
    return f"{total_pay}"
  except:
    messagebox.showerror("Error", "Invalid year/month")
    return "---"



def setup_add_tab(frame):
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
  
  time_frame = tk.LabelFrame(frame, text="Working Hours", padx=10, pady=10)
  time_frame.pack(padx=10, pady=(0, 10), fill="x")
  
  minutes_tuple = tuple(range(0, 60, config.get_pay_interval_minutes()))
  minutes_tuple = tuple(map(lambda x: f"{x:02d}", minutes_tuple))
  
  tk.Label(time_frame, text="Start Time:").grid(row=0, column=0, padx=5, pady=5)
  
  default_time = list(map(int, config.get_default_start_time().split(":")))
  default_start_hour = tk.IntVar(value=default_time[0])
  default_start_minute = tk.IntVar(value=default_time[1])
  
  start_hour = tk.Spinbox(time_frame, width=2, from_=0, to=23, textvariable=default_start_hour)
  start_hour.grid(row=0, column=1, padx=5, pady=5)
  
  tk.Label(time_frame, text=":").grid(row=0, column=2, padx=5, pady=5)
  
  start_minute = tk.Spinbox(time_frame, width=2, values=minutes_tuple, textvariable=default_start_minute, wrap=True)
  start_minute.grid(row=0, column=3, padx=5, pady=5)
  
  
  tk.Label(time_frame, text="End Time:").grid(row=1, column=0, padx=5, pady=5)
  
  default_time = list(map(int, config.get_default_end_time().split(":")))
  default_end_hour = tk.IntVar(value=default_time[0])
  default_end_minute = tk.IntVar(value=default_time[1])
  
  end_hour = tk.Spinbox(time_frame, width=2, from_=0, to=23, textvariable=default_end_hour)
  end_hour.grid(row=1, column=1, padx=0, pady=5)
  
  tk.Label(time_frame, text=":").grid(row=1, column=2, padx=0, pady=5)
  
  end_minute = tk.Spinbox(time_frame, width=2, values=minutes_tuple, textvariable=default_end_minute, wrap=True)
  end_minute.grid(row=1, column=3, padx=0, pady=5)
  
  tk.Button(frame,
            text="Add Workday",
            command=lambda: add_workday(cal.get_date(),
                                        f"{start_hour.get()}:{start_minute.get()}", 
                                        f"{end_hour.get()}:{end_minute.get()}"
                                        ),
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
  
  def on_enter_key():
    add_workday(cal.get_date(), f"{start_hour.get()}:{start_minute.get()}", f"{end_hour.get()}:{end_minute.get()}")
  
  frame.bind('<Return>', lambda event: on_enter_key())
  
  

def setup_delete_tab(frame):
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
  
  tk.Button(frame,
            text="Delete Workday",
            command=lambda: remove_workday(cal.get_date()),
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
  
  frame.bind('<Return>', lambda event: remove_workday(cal.get_date()))

def setup_paying_tab(frame):
  default_year, default_month = get_current_date().split("-")
  
  date_frame = tk.LabelFrame(frame, text="Select Date", padx=10, pady=10)
  date_frame.pack(padx=10, pady=10, fill="x")
  
  date_frame.grid_columnconfigure(0, weight=1)
  date_frame.grid_columnconfigure(1, weight=1)
  date_frame.grid_columnconfigure(2, weight=1)
  date_frame.grid_columnconfigure(3, weight=1)
  date_frame.grid_columnconfigure(4, weight=1)
  date_frame.grid_columnconfigure(5, weight=1)

  tk.Label(date_frame, text="Year:", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="e")
  year = tk.Entry(date_frame, font=("Arial", 14, "bold"), width=5)
  year.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="w")
  year.insert(0, default_year)
  
  tk.Label(date_frame, text="Month:", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=(0, 0), pady=5, sticky="e")
  month = tk.Entry(date_frame, font=("Arial", 14, "bold"), width=5)
  month.grid(row=0, column=4, padx=(5, 0), pady=5, sticky="w")
  month.insert(0, default_month)

  pay_frame = tk.LabelFrame(frame, text="Total Paying", padx=10, pady=10)
  pay_frame.pack(padx=10, pady=0, fill="x")

  pay_frame.grid_columnconfigure(0, weight=1)
  pay_frame.grid_columnconfigure(1, weight=1)
  pay_frame.grid_columnconfigure(2, weight=1)
  pay_frame.grid_columnconfigure(3, weight=2)
  


  tk.Label(pay_frame, text="Total Paying", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
  total_paying = tk.Label(pay_frame, text="---", font=("Arial", 14, "bold"))
  total_paying.grid(row=0, column=1, padx=5, pady=5, sticky="w")
  tk.Button(frame,
            text="Get Paying",
            command=lambda: total_paying.config(text=get_monthly_pay(year.get(), month.get())),
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
  
  def on_enter_key():
    total_paying.config(text=get_monthly_pay(year.get(), month.get()))

  frame.bind('<Return>', lambda event: on_enter_key())
  

root = tk.Tk()
root.title(u"Baito")
root.geometry("450x450")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

tab_add = ttk.Frame(notebook)
tab_delete = ttk.Frame(notebook)
tab_paying = ttk.Frame(notebook)

notebook.add(tab_add, text='Add Workday')
notebook.add(tab_delete, text='Delete Workday')
notebook.add(tab_paying, text='View Paying')

setup_add_tab(tab_add)
setup_delete_tab(tab_delete)
setup_paying_tab(tab_paying)


root.mainloop()
