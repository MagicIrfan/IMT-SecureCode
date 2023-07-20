import ctypes


def is_dep_enabled():
    try:
        kernel32 = ctypes.windll.kernel32
        dep_enabled = ctypes.c_int(0)
        if kernel32.GetProcessDEPPolicy(-1, ctypes.byref(dep_enabled), None):
            return dep_enabled.value == 1
    except Exception as e:
        print("Error checking DEP status:", e)
    return False


def subscribe_to_dep():
    try:
        # Get a handle to the current process
        process_handle = ctypes.windll.kernel32.GetCurrentProcess()
        # Enable DEP for the current process
        dep_enabled = ctypes.c_int(1)
        ctypes.windll.kernel32.SetProcessDEPPolicy(dep_enabled)
        ctypes.windll.kernel32.CloseHandle(process_handle)
    except Exception as e:
        print("Error subscribing to DEP:", e)
