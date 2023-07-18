import configparser


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
