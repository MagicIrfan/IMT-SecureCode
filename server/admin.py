import ctypes
import sys


def run_as_admin(command_line=None, wait=True):
    """Run the current script with administrative privileges."""
    # If no command line is specified, use the current script's full path
    if command_line is None:
        command_line = [sys.executable] + sys.argv

    # Try to run with elevated privileges
    try:
        shell32 = ctypes.windll.shell32
        shell32.ShellExecuteW(None, "runas", *command_line, None, 1)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Launch the privileged script with administrative privileges
    run_as_admin(["python", "server.py"] + sys.argv[1:])
