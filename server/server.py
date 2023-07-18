import socketserver
import datetime
import platform
import win32api
from utils.command import Command
from utils.parser import read_config
from systemtime import SYSTEMTIME
import http.server


# Classe pour gérer les demandes de clients distants
class NetworkClockRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = self.request.recv(1024).decode()

        # Vérification de la demande
        if request.startswith(Command.GET_TIME.value):
            format_string = request.split(":")[1]
            self.handle_get_time(format_string)
        elif request.startswith(Command.SET_TIME.value):
            new_time = request.split(":")[1]
            self.handle_set_time(new_time)
        else:
            self.request.send("Invalid request.".encode())

    def handle_get_time(self, format_string):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.request.send(formatted_time.encode())

    def handle_set_time(self, new_time):
        try:
            # datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            print(new_time)
            # Check the platform and call the appropriate function
            platform_name = platform.system()
            if platform_name == 'Windows':
                return self.set_system_time_windows(new_time)
            else:
                return self.set_system_time_unix(new_time)
        except ValueError:
            print("Invalid date and time format.")
            return False
        # Function to set the system time on Windows

    def set_system_time_windows(self, new_time):
        try:
            # Parse new_time and convert it to a SYSTEMTIME structure
            year, month, day, hour, minute, second = map(int, new_time.split("-"))
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

    # Function to set the system time on non-Windows systems (Linux, macOS, etc.)
    def set_system_time_unix(self, new_time):
        try:
            # Use the 'date' command to set the system time
            import subprocess
            subprocess.run(['date', '-s', new_time], check=True)
            return True
        except Exception as e:
            print("Error:", e)
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
