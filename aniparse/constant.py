import re

OPEN_BRACKETS = (
    "(",  # U+0028 LEFT PARENTHESIS
    "[",  # U+005B LEFT SQUARE BRACKET
    "{",  # U+007B LEFT CURLY BRACKET
    "\u300C",  # Corner bracket
    "\u300E",  # White corner bracket
    "\u3010",  # Black lenticular bracket
    "\uFF08",  # Fullwidth parenthesis
)

CLOSE_BRACKETS = (
    ")",  # U+0029 Right parenthesis
    "]",  # U+005D Right square bracket
    "}",  # U+007D Right curly bracket
    "\u300D",  # Corner bracket
    "\u300F",  # White corner bracket
    "\u3011",  # Black lenticular bracket
    "\uFF09",  # Fullwidth right parenthesis
)

BRACKETS = OPEN_BRACKETS + CLOSE_BRACKETS

DASHES: str = "-\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uFE58\uFE63\uFF0D"
DELIMITERS = f"._+ {DASHES}"

RANGE_TOTAL = "of"
RANGE_SEPARATOR = "~&+ "
DISAMBIGUATION_WORDS = {"OF", "THE", "PART"}

CHECKSUM_PLACEHOLDER = "<CHECKSUM>"

ORDINALS = {
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

CONTEXT_DELIMITER = DASHES
