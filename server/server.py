import json
import socketserver
import datetime
import platform
import win32api
from utils.command import Command
from utils.parser import read_config
from systemtime import SYSTEMTIME
import http.server
from datetime import date, datetime
from dateutil.parser import parse


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
            # datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            print(new_time)
            # Check the platform and call the appropriate function
            platform_name = platform.system()
            if platform_name == 'Windows':
                return self.set_system_time_windows(new_time)
            else:
                return False
        except ValueError:
            print("Invalid date and time format.")
            return False
        # Function to set the system time on Windows

    def set_system_time_windows(self, new_time):
        try:
            # Parse new_time and convert it to a SYSTEMTIME structure
            year,month,day = new_time.get("date").split("-")
            hour = new_time.get("hour")
            minute = new_time.get("minute")
            second = new_time.get("second")
            system_time = SYSTEMTIME(year, month, day, hour, minute, second, 0)

            # Call the SetSystemTime function to set the system time
            if win32api.SetSystemTime(system_time.wYear, system_time.wMonth, 0,
                                      system_time.wDay, system_time.wHour,
                                      system_time.wMinute, system_time.wSecond,
                                      system_time.wMilliseconds):
                self.request.send("oui".encode())
                return True
            else:
                self.request.send("non".encode())
                return False
        except Exception as e:
            print("Error:", e)
            return False

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
