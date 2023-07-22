import ctypes
import sys


def run_as_admin(script_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
        return True
    except Exception as e:
        print("Error:", e)
        return False


