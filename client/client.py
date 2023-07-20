import os
import sys

from controller import NCController


if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Ajouter le chemin du répertoire "utils" au sys.path
    utils_dir = os.path.join(parent_dir, "utils")
    sys.path.append(utils_dir)
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

