import sys

from controller import NCController
from utils.config_parser import *
from utils.dep_utils import *


if __name__ == '__main__':
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

