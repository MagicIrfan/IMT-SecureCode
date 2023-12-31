import json
import os
import sys
from datetime import date
from tkinter import messagebox

from model import NCModel
from view import NCView
from get_time_command import GetTimeCommand
import socket

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ajouter le chemin du répertoire "utils" au sys.path
utils_dir = os.path.join(parent_dir, "utils")
response_dir = os.path.join(utils_dir, "response")
sys.path.append(utils_dir)
sys.path.append(response_dir)
from date_utils import *
from admin import *
from socket_utils import *


class NCController:
    def __init__(self, _ip, _port):
        self.view = NCView()
        self.model = NCModel()
        self.ip, self.port = _ip, _port
        self.create_bindings()
        self.view.create_widgets(self.model)
        self.view.mainloop()

    def create_bindings(self):
        self.view.get_time_button.config(command=self.get_time)
        self.view.set_time_button.config(command=self.set_time)
        self.model.current_time.trace_add('write', self.update_time_label)
        self.model.date_var.set(date.today().isoformat())

    def send_request(self, request):
        try:
            # Création du socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, self.port))

            # Envoi de la demande au serveur
            client_socket.send(request.encode())

            # Réception de la réponse du serveur
            response = receive_data(client_socket)

            # Fermeture du socket client
            client_socket.close()

            # Retour de la réponse
            return response
        except ConnectionRefusedError:
            messagebox.showerror("Connection error", "Unable to connect to server")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    # Fonction pour envoyer une demande au serveur et récupérer la réponse
    def get_time(self):
        date_format = self.model.get_date_format()
        # Create a dictionary with the request data
        get_command = GetTimeCommand(date_format)

        # Convert the request data to a JSON string
        request_json = str(get_command)

        # Send the JSON request
        responses = self.send_request(request_json)

        if responses:
            for response_json in responses:
                # Parse the JSON response
                response_data = json.loads(response_json)
                if response_data.get("type") == "OK":
                    current_time = response_data.get("body")
                    # Update the model with the current time
                    self.model.current_time.set(current_time)
                elif response_data.get("type") == "ERROR":
                    messagebox.showerror("Error", response_data.get("body"))

    def set_time(self):
        date = self.model.get_date()
        hour = self.model.get_hour()
        minute = self.model.get_minute()
        second = self.model.get_second()
        if is_datetime_valid(date, hour, minute, second):
            server_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server")
            internal_directory = os.path.join(server_directory, "internal")
            time_changer_path = os.path.join(internal_directory, "time_changer.py")
            command = f"{time_changer_path} {date} {hour} {minute} {second}"
            if run_as_admin(command):
                messagebox.showinfo("Information", "System time has changed !")
            else:
                messagebox.showerror("Error", "Error when changing system time")
        else:
            messagebox.showerror("Error", "Error when changing system time")

    def update_time_label(self, *args):
        self.view.time_label.config(text="Current time : " + self.model.current_time.get())
