import ctypes
import sys
import datetime
import win32api


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


class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", ctypes.c_uint16),
        ("wMonth", ctypes.c_uint16),
        ("wDay", ctypes.c_uint16),
        ("wDayOfWeek", ctypes.c_uint16),
        ("wHour", ctypes.c_uint16),
        ("wMinute", ctypes.c_uint16),
        ("wSecond", ctypes.c_uint16)
    ]


def set_time(date, hour, minute, second):
    try:
        # Parse new_time and convert it to a SYSTEMTIME structure
        year, month, day = date.split("-")
        # Call the SetSystemTime function to set the system time
        local_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        utc_time = local_time.astimezone(datetime.timezone.utc)
        # Call the SetSystemTime function to set the system time
        if win32api.SetSystemTime(utc_time.year, utc_time.month, utc_time.weekday(),
                                  utc_time.day, utc_time.hour,
                                  utc_time.minute, utc_time.second,
                                  0):
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False


if __name__ == '__main__':
    if not is_dep_enabled():
        subscribe_to_dep()
    if len(sys.argv) != 5:
        sys.exit(1)
    print(f"{sys.argv[1]} {sys.argv[2]} {sys.argv[3]} {sys.argv[4]}")
    set_time(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
