import configparser
import ipaddress
import os


def read_config():
    # Initialize the configparser
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Get the 'server' section
    server_section = config['server']
    # Retrieve the 'ip' and 'port' settings
    ip = server_section.get('ip', fallback='127.0.0.1')
    port = server_section.getint('port', fallback=12345)

    return ip, port


def config_file_exists():
    return os.path.isfile('config.ini') or os.access('config.ini', os.R_OK)


def config_is_valid(ip, port):
    # Check if the IP is valid
    try:
        ipaddress.IPv4Address(ip)  # Raises an exception if the IP is invalid
    except ipaddress.AddressValueError:
        print(f"Invalid IP address: {ip}")
        return False

    # Check if the port is within a valid range (e.g., 1 to 65535)
    if not (1 <= port <= 65535):
        print(f"Invalid port number: {port}. Port must be in the range 1-65535.")
        return False

    # If all checks pass, the configuration is considered valid
    return True
