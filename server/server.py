import json
import socketserver
import datetime
from utils.command import Command
from utils.parser import read_config
from datetime import date, datetime
from dateutil.parser import parse
from time_changer import set_time


# Classe pour gérer les demandes de clients distants
class NetworkClockRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request_json = self.request.recv(1024).decode()

        try:
            # Parse the JSON request
            request_data = json.loads(request_json)
            command = request_data.get("command")

            if command == Command.GET_TIME.value:
                format_string = request_data.get("date_format")
                self.handle_get_time(format_string)
            elif command == Command.SET_TIME.value:
                new_time = request_data.get("time")
                self.handle_set_time(new_time)
            else:
                self.request.send("Invalid request.".encode())

        except json.JSONDecodeError:
            self.request.send("Invalid JSON request.".encode())

    def handle_get_time(self, format_string):
        current_time = datetime.now()
        print(current_time)
        if self.is_valid_date_format(format_string):
            formatted_time = current_time.strftime(format_string)
        else:
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Create a dictionary with the response data
        response_data = {
            "current_time": formatted_time
        }

        # Convert the response data to a JSON string
        response_json = json.dumps(response_data)

        # Send the JSON response
        self.request.send(response_json.encode())

    def handle_set_time(self, new_time):
        try:
            return self.set_system_time_windows(new_time)
        except ValueError:
            print("Invalid date and time format.")
            return False
        # Function to set the system time on Windows

    def set_system_time_windows(self, new_time):
        if set_time(new_time):
            self.request.send("oui".encode())
        else:
            self.request.send("non".encode())


    def is_valid_date_format(self, date_format):
        current_time = datetime.now()
        formatted_time = current_time.strftime(date_format)

        try:
            parse(formatted_time)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    # Get the TCP port from the configuration file
    ip, port = read_config()
    server_address = (ip, port)
    # Création du serveur
    server = socketserver.ThreadingTCPServer(server_address, NetworkClockRequestHandler)
    print("Network Clock application is running.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()
