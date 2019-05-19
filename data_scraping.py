
import json
import re

from paths import *


def _get_birth_from_description(description):
    """Result is int"""
    description_lines = description.splitlines()

    # birth is at the first line of description
    if 0 < len(description_lines):
        re_result = re.search(r"[Uu]r.*?(\d{3,})", description_lines[0])
    else:
        return None

    if re_result is not None:
        birth_year = int(re_result.group(1))
    else:
        return None

    # if there's 'p.n.e' in the line it probably mean it is BC'
    if 0 < len(description_lines):
        pne = re.search(r"p[.]n[.]e", description_lines[0])
        if pne is not None:
            return -birth_year
    return birth_year


def _get_death_from_description(description):
    """Result is int"""
    description_lines = description.splitlines()

    if 1 < len(description_lines):
        re_result = re.search(r"[Zz]m.*?(\d{3,})", description_lines[1])
    else:
        return None

    if re_result is not None:
        death_year = int(re_result.group(1))
    else:
        return None

    if 0 < len(description_lines):
        pne = re.search(r"p[.]n[.]e", description_lines[1])
        if pne is not None:
            return -death_year
    return death_year


def _remove_empty_lines(string_with_empty_lines):
    return "".join([s for s in string_with_empty_lines.strip().splitlines(True) if s.strip()])


def _set_missing_date(data, author, birth_year, death_year):
    data[author] = {"birth_year": birth_year, "death_year": death_year}


def _manually_set_missing_dates(data):
    """Can't scrap all the dates, one solution is to manually complete the dates"""
    _set_missing_date(data, "Homer", -750, -750)
    _set_missing_date(data, "\u015awiatope\u0142k Karpi\u0144ski", 1909, 1940)
    _set_missing_date(data, "Patrycja Nowak", 1980, None)  # not sure about this
    _set_missing_date(data, "Jacek Posiad\u0142o", 1964, None)
    _set_missing_date(data, "Edward Redli\u0144ski", 1940, None)
    _set_missing_date(data, "Marek Aureliusz", 121, 180)
    _set_missing_date(data, "Owidiusz", -43, 17)
    _set_missing_date(data, "Wergiliusz", -70, -19)


def scrap_authors_info():
    """Year is saved as int"""
    with open(authors_info_raw_path, 'r') as file:
        data = json.load(file)

    result = {}
    for author_name, author_data in data.items():
        # remove empty lines from description
        description = author_data['description']
        description = _remove_empty_lines(description)

        birth_year = _get_birth_from_description(description)
        death_year = _get_death_from_description(description)

        result[author_name] = {"birth_year": birth_year, "death_year": death_year}

    _manually_set_missing_dates(result)

    with open(authors_info_ready_path, 'w') as file:
        json.dump(result, file, indent=4)
