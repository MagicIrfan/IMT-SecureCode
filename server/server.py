import json
import socketserver
import datetime
import sys

from utils.command import Command
from utils.config_parser import *
from utils.date_utils import *
from utils.admin import *


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
        if is_valid_date_format(format_string):
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
            dates = new_time.get("date")
            hour = new_time.get("hour")
            minute = new_time.get("minute")
            second = new_time.get("second")
            if run_as_admin("python {}".format(f"{os.getcwd()}\\server\\time_changer.py {dates} {hour} {minute} {second}")):
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                self.request.send(formatted_time.encode())
        except ValueError:
            print("Invalid date and time format.")
            return False
        # Function to set the system time on Windows


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
