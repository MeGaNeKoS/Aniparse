import re
from typing import Union

import unicodedata

DASHES = "-\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uFE58\uFE63\uFF0D"
ESCAPED_DASHES = re.escape(DASHES)


def find_non_number_in_string(string) -> Union[int, None]:
    any_number = [char.isdigit() for char in string]
    if not all(any_number):
        return any_number.index(False)
    return None


def find_number_in_string(string) -> Union[int, None]:
    any_number = [char.isdigit() for char in string]
    if any(any_number):
        return any_number.index(True)
    return None


def get_number_from_ordinal(content) -> Union[str, None]:
    ordinals = {
        '1st': '1', 'First': '1',
        '2nd': '2', 'Second': '2',
        '3rd': '3', 'Third': '3',
        '4th': '4', 'Fourth': '4',
        '5th': '5', 'Fifth': '5',
        '6th': '6', 'Sixth': '6',
        '7th': '7', 'Seventh': '7',
        '8th': '8', 'Eighth': '8',
        '9th': '9', 'Ninth': '9'
    }
    return ordinals.get(str(content).lower(), None)


def is_crc32(string) -> bool:
    if len(string) != 8:
        return False
    try:
        int(string, 16)
    except ValueError:
        return False
    return True


def is_dash_character(string) -> bool:
    return string in DASHES


def is_latin_char(char):
    return is_latin_char.cache.setdefault(char, 'LATIN' in unicodedata.name(char))


is_latin_char.cache = {}


def is_mostly_latin_string(string: str):
    if len(string) == 0:
        return False
    latin_length = len([char for char in string if is_latin_char(char)])
    return latin_length / len(string) >= 0.5


def is_potential_number(text) -> bool:
    """
    1.0 -> False
    1 -> True
    1.1 -> True
    1.1.1 -> False
    01 -> True
    01.1 -> False
    """
    try:
        f_text = float(text)
        # Evangelion 1.0: You Are (Not) Alone
        if f_text.is_integer():
            return True
        if str(f_text) != text:
            return False
        return True
    except ValueError:
        return False


def is_resolution(string) -> bool:
    pattern = '\\d{3,4}([pP]|([xX\u00D7]\\d{3,4}))$'
    return bool(re.match(pattern, string))
