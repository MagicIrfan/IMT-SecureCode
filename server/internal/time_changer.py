import os
import datetime
import win32api
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
utils_dir = os.path.join(parent_dir, "utils")
sys.path.append(utils_dir)
from dep_utils import is_dep_enabled, subscribe_to_dep
from date_utils import is_datetime_valid
from privilege import adjust_privileges


def set_time(date_, hour_, minute_, second_):
    try:
        year, month, day = map(int, date_.split("-"))

        # Call the SetSystemTime function to set the system time
        local_time = datetime.datetime(year, month, day, hour_, minute_, second_)
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
        return False


if __name__ == '__main__':
    if not is_dep_enabled():
        subscribe_to_dep()
    adjust_privileges(["SeSystemtimePrivilege"])

    if len(sys.argv) != 5:
        sys.exit(1)

    date = sys.argv[1]
    hour = int(sys.argv[2])
    minute = int(sys.argv[3])
    second = int(sys.argv[4])

    if not is_datetime_valid(date, hour, minute, second):
        sys.exit(1)
    set_time(date, hour, minute, second)
