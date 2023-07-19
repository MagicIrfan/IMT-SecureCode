import ctypes

# DEP constants
PROCESS_DEP_ENABLE = 1
PROCESS_DEP_DISABLE_ATL_THUNK_EMULATION = 2


def is_dep_enabled():
    try:
        kernel32 = ctypes.windll.kernel32
        dep_enabled = ctypes.c_int(0)
        if kernel32.GetProcessDEPPolicy(-1, ctypes.byref(dep_enabled), None):
            return dep_enabled.value == PROCESS_DEP_ENABLE
    except Exception as e:
        print("Error checking DEP status:", e)
    return False


def subscribe_to_dep():
    try:
        # Get a handle to the current process
        process_handle = ctypes.windll.kernel32.GetCurrentProcess()

        # Enable DEP for the current process
        ctypes.windll.kernel32.SetProcessDEPPolicy(PROCESS_DEP_ENABLE)

        # Close the process handle
        ctypes.windll.kernel32.CloseHandle(process_handle)

        return True
    except Exception as e:
        print("Error subscribing to DEP:", e)
        return False
