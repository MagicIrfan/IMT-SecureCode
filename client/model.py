import tkinter as tk
from datetime import datetime


class NCModel:
    def __init__(self):
        self.date_var = tk.StringVar()
        self.hour_var = tk.IntVar()
        self.minute_var = tk.IntVar()
        self.second_var = tk.IntVar()
        self.date_format = tk.StringVar(value="%Y-%m-%d %H:%M:%S")
        self.current_time = tk.StringVar(value=datetime.now().strftime(self.get_date_format()))

    # Getters
    def get_date(self):
        return self.date_var.get()

    def get_hour(self):
        return self.hour_var.get()

    def get_minute(self):
        return self.minute_var.get()

    def get_second(self):
        return self.second_var.get()

    def get_date_format(self):
        return self.date_format.get()

    # Setters
    def set_date(self, value):
        self.date_var.set(value)

    def set_hour(self, value):
        self.hour_var.set(value)

    def set_minute(self, value):
        self.minute_var.set(value)

    def set_second(self, value):
        self.second_var.set(value)

    def set_date_format(self, value):
        self.date_format.set(value)
