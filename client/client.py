from tkinter import messagebox
import socket
from parser import read_config
from networkclockapp import NCView


class Client:
    def __init__(self):
        self.view = NCView()
        self.ip, self.port = '127.0.0.1', 12345
        self.view.get_time_button.config(command=self.get_time)
        self.view.set_time_button.config(command=self.set_time)
        self.view.mainloop()

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
        request = f"GET_TIME:{format_string}"
        response = self.send_request(request)
        if response:
            self.view.current_time.set(response)

    def set_time(self):
        year = self.view.get_year()
        month = self.view.get_month()
        day = self.view.get_day()
        hour = self.view.get_hour()
        minute = self.view.get_minute()
        second = self.view.get_second()

        new_time = f"{year}-{month}-{day}-12-12-12"
        request = f"SET_TIME:{new_time}"
        response = self.send_request(request)
        if response:
            messagebox.showinfo("Changement d'heure", response)


if __name__ == '__main__':
    client = Client()

