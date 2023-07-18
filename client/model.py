import tkinter as tk


class NCModel:
    def __init__(self):
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.second_var = tk.StringVar()
        self.current_time = tk.StringVar()

    # Getters
    def get_year(self):
        return self.year_var.get()

    def get_month(self):
        return self.month_var.get()

    def get_day(self):
        return self.day_var.get()

    def get_hour(self):
        return self.hour_var.get()

    def get_minute(self):
        return self.minute_var.get()

    def get_second(self):
        return self.second_var.get()

    # Setters
    def set_year(self, value):
        self.year_var.set(value)

    def set_month(self, value):
        self.month_var.set(value)

    def set_day(self, value):
        self.day_var.set(value)

    def set_hour(self, value):
        self.hour_var.set(value)

    def set_minute(self, value):
        self.minute_var.set(value)

    def set_second(self, value):
        self.second_var.set(value)
