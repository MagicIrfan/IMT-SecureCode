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
        format_string = "%Y-%m-%d %H:%M:%S"
        request = f"{Command.GET_TIME.value}:{format_string}"
        response = self.send_request(request)
        if response:
            self.model.current_time.set(response)

    def set_time(self):
        year = self.model.get_year()
        month = self.model.get_month()
        day = self.model.get_day()
        hour = self.model.get_hour()
        minute = self.model.get_minute()
        second = self.model.get_second()

        new_time = f"{year}-{month}-{day}-12-12-12"
        request = f"{Command.SET_TIME.value}:{new_time}"
        response = self.send_request(request)
        if response:
            messagebox.showinfo("Changement d'heure", response)

    def update_time_label(self, *args):
        self.view.time_label.config(text="Heure actuelle : " + self.model.current_time.get())
