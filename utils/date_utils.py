from datetime import datetime

import dateutil
from dateutil.parser import parse


def is_valid_date_format(date_format):
    current_time = datetime.now()
    formatted_time = current_time.strftime(date_format)

    try:
        parse(formatted_time)
        return True
    except ValueError:
        return False


def is_date_valid(date):
    try:
        # Essayez de convertir la chaîne de date en objet date
        # Si la conversion réussit, alors la date est valide, sinon elle lève une exception
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_hours_valid(hour):
    try:
        hour = int(hour)
        return 0 <= hour <= 23
    except ValueError:
        return False


def is_minutes_valid(minutes):
    try:
        minutes = int(minutes)
        return 0 <= minutes <= 59
    except ValueError:
        return False


def is_seconds_valid(seconds):
    try:
        seconds = int(seconds)
        return 0 <= seconds <= 59
    except ValueError:
        return False


def is_datetime_valid(date, hours, minutes, seconds):
    return is_date_valid(date) \
        and is_hours_valid(hours) \
        and is_minutes_valid(minutes) \
        and is_seconds_valid(seconds)
