import socketserver
import datetime
import json
import os
import sys
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
from privilege import adjust_privileges
from dep_utils import *
from controller import NCController


def start_client(_ip, _port):
    client = NCController(_ip, _port)


class NetworkClockRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        for request_json in receive_data(self.request):
            if len(request_json) > 0:
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
            else:
                self.request.send("Data is empty".encode())

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
    if not is_dep_enabled():
        subscribe_to_dep()
    adjust_privileges()
    if not config_file_exists():
        sys.exit(1)
    # Get the TCP port from the configuration file
    ip, port = read_config()
    if not config_is_valid(ip, port):
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
