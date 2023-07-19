import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar


class NCView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock")
        self.get_time_button = tk.Button(self, text="Obtenir l'heure actuelle")
        self.set_time_button = tk.Button(self, text="Définir la date et l'heure système")

    def create_widgets(self, model):
        # Labels and Entry/Combobox widgets
        calendar = Calendar(self, selectmode='day',
                            calendar_height=100,  # Adjust calendar height
                            calendar_width=100,
                            textvariable=model.date_var)

        hour_label = tk.Label(self, text="Heure :")
        hour_spinbox = tk.Spinbox(self, from_=0, to=23, textvariable=model.hour_var)

        minute_label = tk.Label(self, text="Minutes :")
        minute_spinbox = tk.Spinbox(self, from_=0, to=59, textvariable=model.minute_var)

        second_label = tk.Label(self, text="Secondes :")
        second_spinbox = tk.Spinbox(self, from_=0, to=59, textvariable=model.second_var)

        date_format_label = tk.Label(self, text="Format de date :")
        date_format_entry = tk.Entry(self, textvariable=model.date_format, width=50)  # Add the Entry widget for date format

        self.time_label = tk.Label(self, text="Heure actuelle : " + model.current_time.get())
        self.time_label.config(font=("Arial", 14, "bold"))

        # Grid layout
        calendar.grid(row=0, column=0, columnspan=6, padx=10, pady=5)  # Spanning the entire width
        hour_label.grid(row=1, column=0, padx=10, pady=5)
        hour_spinbox.grid(row=1, column=1, padx=10, pady=5)
        minute_label.grid(row=1, column=2, padx=10, pady=5)
        minute_spinbox.grid(row=1, column=3, padx=10, pady=5)
        second_label.grid(row=1, column=4, padx=10, pady=5)
        second_spinbox.grid(row=1, column=5, padx=10, pady=5)
        date_format_label.grid(row=2, column=0, padx=10, pady=5)  # Add the label for date format
        date_format_entry.grid(row=2, column=1, columnspan=5, padx=10, pady=5)  # Adjust columnspan to span all entries
        self.get_time_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.set_time_button.grid(row=3, column=3, columnspan=3, padx=10, pady=5)
        self.time_label.grid(row=4, column=0, columnspan=6, padx=10, pady=5)

        # Adjust the grid weights to center the calendar widget
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        calendar.bind("<<CalendarSelected>>", self.on_calendar_selected)

    def on_calendar_selected(self, event):
        # This method will be executed when the user selects a date in the calendar
        date_selected = event.widget.selection_get()
        print("Date selected:", date_selected)