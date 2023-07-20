import ctypes


def run_as_admin(script_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", script_path, None, 1)
        return True
    except Exception as e:
        print("Error :", e)
        return False


