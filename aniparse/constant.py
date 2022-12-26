import re
from typing import Literal, Tuple

OPEN_BRACKETS: Tuple[Literal[
    "(", "[", "{", "\u300C", "\u300E", "\u3010", "\uFF08"], ...] = (
    "(",  # U+0028 LEFT PARENTHESIS
    "[",  # U+005B LEFT SQUARE BRACKET
    "{",  # U+007B LEFT CURLY BRACKET
    "\u300C",  # Corner bracket
    "\u300E",  # White corner bracket
    "\u3010",  # Black lenticular bracket
    "\uFF08",  # Fullwidth parenthesis
)

CLOSE_BRACKETS: Tuple[Literal[
    ")", "]", "}", "\u300D", "\u300F", "\u3011", "\uFF09"], ...] = (
    ")",  # U+0029 Right parenthesis
    "]",  # U+005D Right square bracket
    "}",  # U+007D Right curly bracket
    "\u300D",  # Corner bracket
    "\u300F",  # White corner bracket
    "\u3011",  # Black lenticular bracket
    "\uFF09",  # Fullwidth right parenthesis
)

BRACKETS = OPEN_BRACKETS + CLOSE_BRACKETS

OPEN_BRACKETS_PATTERN = '|'.join(re.escape(b) for b in OPEN_BRACKETS)
CLOSE_BRACKETS_PATTERN = '|'.join(re.escape(b) for b in CLOSE_BRACKETS)
BRACKET_PATTERN = f'{OPEN_BRACKETS_PATTERN}|{CLOSE_BRACKETS_PATTERN}'

DASHES: str = "-\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uFE58\uFE63\uFF0D"
