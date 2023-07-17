import socketserver
import datetime


# Classe pour gérer les demandes de clients distants
class NetworkClockRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = self.request.recv(1024).decode()

        # Vérification de la demande
        if request.startswith("GET_TIME"):
            format_string = request.split(":")[1]
            self.handle_get_time(format_string)
        elif request.startswith("SET_TIME"):
            new_time = request.split(":")[1]
            self.handle_set_time(new_time)
        else:
            self.request.send("Invalid request.".encode())

    def handle_get_time(self, format_string):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(format_string)
        self.request.send(formatted_time.encode())

    def handle_set_time(self, new_time):
        try:
            datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            # Code pour définir la date et l'heure système ici
            self.request.send("Date and time have been set successfully.".encode())
        except ValueError:
            self.request.send("Invalid date and time format. Please use the format: YYYY-MM-DD HH:MM:SS".encode())
