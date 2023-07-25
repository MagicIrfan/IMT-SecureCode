import socketserver
import datetime
import json
import os
import sys
from datetime import date
from tkinter import messagebox
import socket
import threading

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ajouter le chemin du répertoire "utils" au sys.path
utils_dir = os.path.join(parent_dir, "utils")
client_dir = os.path.join(parent_dir, "client")

response_dir = os.path.join(utils_dir, "response")
sys.path.append(utils_dir)
sys.path.append(response_dir)
sys.path.append(client_dir)
from config_parser import *
from date_utils import *
from admin import *
from response.ok_reponse import OKResponse
from response.error_response import ErrorResponse
from socket_utils import *
from model import NCModel
from view import NCView
from get_time_command import GetTimeCommand
from privilege import adjust_privileges
from dep_utils import *


def start_client(_ip, _port):
    client = NCController(_ip, _port)


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
        response_json = self.send_request(request_json)

        if response_json:
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


class NetworkClockRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        request_json = receive_data(self.request)
        try:
            # Parse the JSON request
            request_data = json.loads(request_json)
            command = request_data.get("type")
            if command == "GET_TIME":
                format_string = request_data.get("body")
                self.handle_get_time(format_string)
            else:
                self.request.send("Invalid request.".encode())

        except json.JSONDecodeError:
            self.request.send("Invalid JSON request.".encode())

    def handle_get_time(self, format_string):
        current_time = datetime.now()
        if is_valid_date_format(format_string):
            formatted_time = current_time.strftime(format_string)
            response = OKResponse(formatted_time)
        else:
            response = ErrorResponse("Formatted time is incorrect")

        # Convert the response data to a JSON string
        response_json = str(response)
        # Send the JSON response
        self.request.send(response_json.encode())


if __name__ == '__main__':
    if not config_file_exists():
        sys.exit(1)
    # Get the TCP port from the configuration file
    ip, port = read_config()
    if not config_is_valid(ip, port):
        sys.exit(1)
    if not is_dep_enabled():
        subscribe_to_dep()
    if not adjust_privileges():
        sys.exit(1)
    # Start the client in a separate thread
    client_thread = threading.Thread(target=start_client, args=(ip, port))
    client_thread.start()
    # Server creation
    server = socketserver.ThreadingTCPServer((ip, port), NetworkClockRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()
