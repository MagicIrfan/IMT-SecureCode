import os
import sys

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_dir = os.path.join(parent_dir, "server")
    utils_dir = os.path.join(parent_dir, "utils")
    sys.path.append(utils_dir)
    sys.path.append(server_dir)
    from NC import NCController
    from config_parser import *
    from dep_utils import *
    if not config_file_exists():
        sys.exit(1)
    ip, port = read_config()
    if not config_is_valid(ip, port):
        sys.exit(1)
    if not is_dep_enabled():
        subscribe_to_dep()
    else:
        print("DEP is already activated")
    client = NCController(ip, port)

