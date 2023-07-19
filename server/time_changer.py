import win32api
import ctypes
from systemtime import SYSTEMTIME
from utils.dep import *
import runas
import sys



# Ajouter les définitions de structure pour TOKEN_PRIVILEGES
class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.c_ulong),
        ("HighPart", ctypes.c_long)
    ]


class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", ctypes.c_ulong)
    ]


class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", ctypes.c_ulong),
        ("Privileges", LUID_AND_ATTRIBUTES * 1)  # Use 1 for a single privilege, adjust accordingly if more are needed
    ]


# Déclarer une variable globale pour stocker les anciens privilèges
old_privileges = None
SE_PRIVILEGE_ENABLED = 0x00000002
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008


def elevate_privileges():
    try:
        global old_privileges
        # Open the current process token
        token_handle = ctypes.windll.kernel32.OpenProcessToken(-1, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, 0)
        if not token_handle:
            return False

        # Look up the privilege value for "SeDebugPrivilege"
        luid = LUID()
        if not ctypes.windll.advapi32.LookupPrivilegeValueW(None, "SeDebugPrivilege", ctypes.byref(luid)):
            ctypes.windll.kernel32.CloseHandle(token_handle)
            return False

        # Enable the privilege
        tp = TOKEN_PRIVILEGES()
        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

        if not ctypes.windll.advapi32.AdjustTokenPrivileges(token_handle, False, ctypes.byref(tp), ctypes.sizeof(tp),
                                                            None, None):
            ctypes.windll.kernel32.CloseHandle(token_handle)
            return False

        ctypes.windll.kernel32.CloseHandle(token_handle)
        old_privileges = tp
        return True
    except Exception as e:
        print("Error:", e)
        return False


def restore_privileges():
    try:
        global old_privileges

        if old_privileges is None:
            return False

        # Récupérer le handle du token du processus actuel
        token_handle = ctypes.windll.kernel32.OpenProcessToken(-1, TOKEN_ADJUST_PRIVILEGES, 0)
        if not token_handle:
            return False

        # Rétablir les privilèges d'origine en utilisant old_privileges
        if not ctypes.windll.advapi32.AdjustTokenPrivileges(token_handle, False, ctypes.byref(old_privileges), 0, None,
                                                            None):
            ctypes.windll.kernel32.CloseHandle(token_handle)
            return False

        ctypes.windll.kernel32.CloseHandle(token_handle)
        old_privileges = None
        return True
    except Exception as e:
        print("Error:", e)
        return False


def set_time(new_time):
    try:
        # Parse new_time and convert it to a SYSTEMTIME structure
        year, month, day = new_time.get("date").split("-")
        hour = new_time.get("hour")
        minute = new_time.get("minute")
        second = new_time.get("second")
        system_time = SYSTEMTIME(int(year), int(month), int(day), int(hour), int(minute), int(second))

        # Call the SetSystemTime function to set the system time
        if win32api.SetSystemTime(system_time.wYear, system_time.wMonth, 0,
                                  system_time.wDay, system_time.wHour,
                                  system_time.wMinute, system_time.wSecond,
                                  system_time.wMilliseconds):
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False

if __name__== '__main__':
    print("test")

