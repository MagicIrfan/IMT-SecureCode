import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar


class NCView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock")
        self.get_time_button = tk.Button(self, text="Get current time",width=25)
        self.set_time_button = tk.Button(self, text="Set system date",width=25)
        self.resizable(width=False, height=False)

    def create_widgets(self, model):
        # Labels and Entry/Combobox widgets
        calendar = Calendar(self, selectmode='day',
                            calendar_height=100,  # Adjust calendar height
                            calendar_width=100,
                            date_pattern="yyyy-mm-dd",
                            textvariable=model.date_var)

        date_label = tk.Label(self, text="Date")

        hour_label = tk.Label(self, text="Hour")
        hour_spinbox = tk.Spinbox(self, from_=0, to=23, textvariable=model.hour_var)

        minute_label = tk.Label(self, text="Minutes")
        minute_spinbox = tk.Spinbox(self, from_=0, to=59, textvariable=model.minute_var)

        second_label = tk.Label(self, text="Seconds")
        second_spinbox = tk.Spinbox(self, from_=0, to=59, textvariable=model.second_var)

        date_format_label = tk.Label(self, text="Date format")
        date_format_entry = tk.Entry(self, textvariable=model.date_format,
                                     width=50)  # Add the Entry widget for date format

        self.time_label = tk.Label(self, text="Current time : " + model.current_time.get())
        self.time_label.config(font=("Arial", 14, "bold"))

        date_label.grid(row=0, column=0, columnspan=6, padx=10, pady=5)

        # Grid layout
        calendar.grid(row=1, column=0, columnspan=6, padx=10, pady=5)  # Spanning the entire width

        hour_label.grid(row=2, column=0, columnspan=6, padx=10, pady=5)
        hour_spinbox.grid(row=3, column=0, columnspan=6, padx=10, pady=5)

        minute_label.grid(row=4, column=0, columnspan=6, padx=10, pady=5)
        minute_spinbox.grid(row=5, column=0, columnspan=6, padx=10, pady=5)

        second_label.grid(row=6, column=0, columnspan=6, padx=10, pady=5)
        second_spinbox.grid(row=7, column=0, columnspan=6, padx=10, pady=5)

        date_format_label.grid(row=8, column=0, columnspan=6, padx=10, pady=5)  # Add the label for date format
        date_format_entry.grid(row=9, column=0, columnspan=6, padx=10, pady=5)  # Adjust columnspan to span all entries

        self.get_time_button.grid(row=10, column=0, padx=5, pady=5, sticky="ew")
        self.set_time_button.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        self.time_label.grid(row=11, column=0, columnspan=6, padx=10, pady=5)

        # Adjust the grid weights to center the calendar widget
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)