import json
import os
import socketserver
import datetime
import sys
import http.server

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ajouter le chemin du répertoire "utils" au sys.path
utils_dir = os.path.join(parent_dir, "utils")
response_dir = os.path.join(utils_dir, "response")
sys.path.append(utils_dir)
sys.path.append(response_dir)
from config_parser import *
from date_utils import *
from admin import *
from response.ok_reponse import OKResponse
from response.error_response import ErrorResponse


# Classe pour gérer les demandes de clients distants
class NetworkClockRequestHandler(socketserver.BaseRequestHandler):

    def is_local_client(self):
        # Check if the address is the loopback address or if it's an SSH connection
        return self.client_address[0] in ("127.0.0.1", "localhost") or "SSH_CLIENT" in os.environ

    def handle(self):
        request_json = self.request.recv(1024).decode()
        try:
            # Parse the JSON request
            request_data = json.loads(request_json)
            command = request_data.get("type")
            if command == "GET_TIME":
                format_string = request_data.get("body")
                self.handle_get_time(format_string)
            elif command == "SET_TIME":
                new_time = json.loads(request_data.get("body"))
                self.handle_set_time(new_time)
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

    def handle_set_time(self, new_time):
        try:
            if self.is_local_client():
                dates = new_time.get("date")
                hour = new_time.get("hour")
                minute = new_time.get("minute")
                second = new_time.get("second")

                if is_datetime_valid(dates, hour, minute, second):
                    if run_as_admin(
                            f"{os.getcwd()}\\internal\\time_changer.py {dates} {hour} {minute} {second}"):
                        response = OKResponse("System time has changed !")
                    else:
                        response = ErrorResponse("Error when changing system time")
                else:
                    response = ErrorResponse("Error when changing system time")
            else:
                response = ErrorResponse("You are not authorized to perform this action")
            self.request.send(str(response).encode())
        except ValueError:
            return False


if __name__ == '__main__':
    if not config_file_exists():
        sys.exit(1)
    # Get the TCP port from the configuration file
    ip, port = read_config()
    if not config_is_valid(ip, port):
        sys.exit(1)
    # Server creation
    server = socketserver.ThreadingTCPServer((ip, port), NetworkClockRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()
