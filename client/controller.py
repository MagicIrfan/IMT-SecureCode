import json
from datetime import date, datetime
from tkinter import messagebox
import socket
from utils.command import Command
from utils.parser import read_config
from model import NCModel
from view import NCView


class NCController:
    def __init__(self):
        self.view = NCView()
        self.model = NCModel()
        self.ip, self.port = read_config()
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
            response = client_socket.recv(1024).decode()

            # Fermeture du socket client
            client_socket.close()

            # Retour de la réponse
            return response
        except ConnectionRefusedError:
            messagebox.showerror("Erreur de connexion", "Impossible de se connecter au serveur.")
            return None

    # Fonction pour envoyer une demande au serveur et récupérer la réponse
    def get_time(self):
        date_format = self.model.get_date_format()
        # Create a dictionary with the request data
        request_data = {
            "command": Command.GET_TIME.value,
            "date_format": date_format
        }

        # Convert the request data to a JSON string
        request_json = json.dumps(request_data)

        # Send the JSON request
        response_json = self.send_request(request_json)

        if response_json:
            # Parse the JSON response
            response_data = json.loads(response_json)
            current_time = response_data.get("current_time")

            # Update the model with the current time
            self.model.current_time.set(current_time)

    def set_time(self):
        date = self.model.get_date()
        hour = self.model.get_hour()
        minute = self.model.get_minute()
        second = self.model.get_second()
        request_data = {
            "command": Command.SET_TIME.value,
            "time": {
                "date": date,
                "hour": hour,
                "minute": minute,
                "second": second
            }
        }
        # Convert the request data to a JSON string
        request_json = json.dumps(request_data)

        # Send the JSON request
        response_json = self.send_request(request_json)

        if response_json:
            messagebox.showinfo("Changement d'heure", response_json)

    def update_time_label(self, *args):
        self.view.time_label.config(text="Heure actuelle : " + self.model.current_time.get())
