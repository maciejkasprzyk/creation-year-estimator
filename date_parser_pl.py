import re
from datetime import datetime


def month_parse(date_raw):
    """
    Function parsing month name in PL from wolnelektury.pl into integer.
    Returns -1 when month doesn't match
    :param date_raw: date in string format, PL style
    :return: month number (int)
    """
    if date_raw is None:
        return None

    # exclude year
    regex_year = re.search(r"\b[1-2][0-9]{3}\b", date_raw)
    if regex_year is not None:
        date_without_year = date_raw[:regex_year.start()].strip()
    else:
        date_without_year = date_raw

    # exclude day
    regex_day = re.search(r"\b\d{2}\b", date_raw)
    if regex_day is not None:
        month_raw = date_without_year[regex_day.end():]
    else:
        month_raw = date_without_year

    # parse polish month names
    if month_raw.find("sty") != -1:
        month = 1
    elif month_raw.find("lut") != -1:
        month = 2
    elif month_raw.find("mar") != -1:
        month = 3
    elif month_raw.find("kwi") != -1:
        month = 4
    elif month_raw.find("maj") != -1:
        month = 5
    elif month_raw.find("cze") != -1:
        month = 6
    elif month_raw.find("lip") != -1:
        month = 7
    elif month_raw.find("sie") != -1:
        month = 8
    elif month_raw.find("wrz") != -1:
        month = 9
    elif month_raw.find("paź") != -1:
        month = 10
    elif month_raw.find("lis") != -1:
        month = 11
    elif month_raw.find("gru") != -1:
        month = 12
    else:
        month = -1

    return month


def date_parse(date_raw):
    """
    Function parsing date from wolnelektury.pl into date format.
    Returns None if date doesn't match any known style
    :param date_raw: date in string format, PL style
    :return: date in correct format
    """

    if date_raw is None:
        return None

    # extract year
    regex_year = re.search(r"\b[1-2]?[0-9]{3}\b", date_raw)
    if regex_year is not None:
        year = regex_year.group()
    else:
        return None

    # extract day
    regex_day = re.search(r"\b\d{1,2}\b", date_raw)
    if regex_day is not None:
        day = regex_day.group()
    else:
        return None

    # extract month
    month = month_parse(date_raw)
    if month is None or month == -1:
        return None

    date_str = day + "-" + str(month) + "-" + year
    date = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date

