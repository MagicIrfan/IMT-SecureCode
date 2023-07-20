from datetime import datetime
from dateutil.parser import parse


def is_valid_date_format(date_format):
    current_time = datetime.now()
    formatted_time = current_time.strftime(date_format)

    try:
        parse(formatted_time)
        return True
    except ValueError:
        return False
