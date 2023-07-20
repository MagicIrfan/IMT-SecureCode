import os
import datetime
import win32api
import sys


def set_time(date, hour, minute, second):
    try:
        # Parse new_time and convert it to a SYSTEMTIME structure
        year, month, day = map(int, date.split("-"))
        hour, minute, second = map(int, (hour, minute, second))

        # Call the SetSystemTime function to set the system time
        local_time = datetime.datetime(year, month, day, hour, minute, second)
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
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Ajouter le chemin du répertoire "utils" au sys.path
    utils_dir = os.path.join(parent_dir, "utils")
    sys.path.append(utils_dir)
    from dep_utils import is_dep_enabled, subscribe_to_dep

    if not is_dep_enabled():
        subscribe_to_dep()
    if len(sys.argv) != 5:
        sys.exit(1)
    set_time(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
