import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket
from parser import read_config


class NCView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock")

        # Widgets variables
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.second_var = tk.StringVar()
        self.current_time = tk.StringVar()
        self.current_time.trace_add('write', self.update_time_label)
        self.get_time_button = tk.Button(self, text="Obtenir l'heure actuelle")
        self.set_time_button = tk.Button(self, text="Définir la date et l'heure système")
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry/Combobox widgets
        year_label = tk.Label(self, text="Année :")
        year_entry = ttk.Combobox(self, textvariable=self.year_var, values=list(range(2000, 2101)))

        month_label = tk.Label(self, text="Mois :")
        month_entry = ttk.Combobox(self, textvariable=self.month_var, values=list(range(1, 13)))

        day_label = tk.Label(self, text="Jour :")
        day_entry = ttk.Combobox(self, textvariable=self.day_var, values=list(range(1, 32)))

        hour_label = tk.Label(self, text="Heure :")
        hour_entry = ttk.Combobox(self, textvariable=self.hour_var, values=list(range(24)))

        minute_label = tk.Label(self, text="Minutes :")
        minute_entry = ttk.Combobox(self, textvariable=self.minute_var, values=list(range(60)))

        second_label = tk.Label(self, text="Secondes :")
        second_entry = ttk.Combobox(self, textvariable=self.second_var, values=list(range(60)))

        self.time_label = tk.Label(self, text="Heure actuelle : " + self.current_time.get())
        self.time_label.config(font=("Arial", 14, "bold"))

        # Grid layout
        year_label.grid(row=0, column=0, padx=10, pady=5)
        year_entry.grid(row=0, column=1, padx=10, pady=5)

        month_label.grid(row=0, column=2, padx=10, pady=5)
        month_entry.grid(row=0, column=3, padx=10, pady=5)

        day_label.grid(row=0, column=4, padx=10, pady=5)
        day_entry.grid(row=0, column=5, padx=10, pady=5)

        hour_label.grid(row=1, column=0, padx=10, pady=5)
        hour_entry.grid(row=1, column=1, padx=10, pady=5)

        minute_label.grid(row=1, column=2, padx=10, pady=5)
        minute_entry.grid(row=1, column=3, padx=10, pady=5)

        second_label.grid(row=1, column=4, padx=10, pady=5)
        second_entry.grid(row=1, column=5, padx=10, pady=5)

        self.get_time_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        self.set_time_button.grid(row=2, column=3, columnspan=3, padx=10, pady=5)

        self.time_label.grid(row=3, column=0, columnspan=6, padx=10, pady=5)

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

    def update_time_label(self, *args):
        self.time_label.config(text="Heure actuelle : " + self.current_time.get())


