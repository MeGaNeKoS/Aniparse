import re
from typing import Union


def find_first_number(word) -> Union[int, None]:
    """
    Find the first occurrence of a number in a string.

    Parameters:
    - word: The string to search for a number.

    Returns:
    - The index of the first occurrence of a number in the string, or None if no number is found.
    """
    any_number = [char.isdigit() for char in word]
    if any(any_number):
        return any_number.index(True)
    return None


def find_first_alpha(word) -> Union[int, None]:
    """
    Find the first occurrence of a alpha in a string.

    Parameters:
    - word: The string to search for a number.

    Returns:
    - The index of the first occurrence of a number in the string, or None if no number is found.
    """
    any_string = [char.isalpha() for char in word]
    if any(any_string):
        return any_string.index(True)
    return None


def is_resolution(string) -> bool:
    pattern = '\\d{3,4}([ip]|([x\u00D7]\\d{3,4}))$'
    return bool(re.match(pattern, string, flags=re.IGNORECASE))


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
