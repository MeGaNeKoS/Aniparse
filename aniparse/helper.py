from typing import Union

from aniparse import constant


def first_number_lower_than_second(first, second):
    if not is_number(first) or not is_number(second):
        return False
    return float(first) < float(second)


def is_number(string) -> bool:
    """
    Check if the given `Token` object represents a number.

    Args:
        string: The string to check.

    Returns:
        bool: True if the `Token` object represents a number, False otherwise.
    """
    try:
        float(string)
        return True
    except (ValueError, TypeError):
        return False


def is_dash_character(string) -> bool:
    return string in constant.DASHES


def get_number(string) -> Union[int, float, None, str]:
    try:
        f_number = float(string)
        if f_number.is_integer():
            # the string is already an integer of float. "1.0"
            if str(f_number) == string and f_number != 0.0:
                return string
            return int(f_number)
        return f_number
    except ValueError:
        return None


def is_crc32(word) -> bool:
    if len(word) != 8:
        return False
    try:
        int(word, 16)
        return True
    except ValueError:
        return False

