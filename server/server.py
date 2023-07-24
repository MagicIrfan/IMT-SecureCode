import json
import os
import socketserver
import datetime
import sys

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
from socket_utils import *


# Classe pour gérer les demandes de clients distants
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
    # Server creation
    server = socketserver.ThreadingTCPServer((ip, port), NetworkClockRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()
