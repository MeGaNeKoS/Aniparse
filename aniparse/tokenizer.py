from __future__ import unicode_literals, absolute_import

import logging
import re
from typing import Tuple

from aniparse import parser_helper
from aniparse.element import ElementCategory
from aniparse.keyword import KeywordManager
from aniparse.token import TokenCategory, Tokens

logger = logging.getLogger(__name__)

open_brackets = (
    "(",  # U+0028 LEFT PARENTHESIS
    "[",  # U+005B LEFT SQUARE BRACKET
    "{",  # U+007B LEFT CURLY BRACKET
    "\u300C",  # Corner bracket
    "\u300E",  # White corner bracket
    "\u3010",  # Black lenticular bracket
    "\uFF08",  # Fullwidth parenthesis
)

close_brackets = (
    ")",  # U+0029 Right parenthesis
    "]",  # U+005D Right square bracket
    "}",  # U+007D Right curly bracket
    "\u300D",  # Corner bracket
    "\u300F",  # White corner bracket
    "\u3011",  # Black lenticular bracket
    "\uFF09",  # Fullwidth right parenthesis
)

brackets = open_brackets + close_brackets
escaped_open_brackets = [re.escape(bracket) for bracket in open_brackets]
escaped_close_brackets = [re.escape(bracket) for bracket in close_brackets]
escaped_brackets = '|'.join(escaped_open_brackets + escaped_close_brackets)


def invert_string_brackets(text) -> Tuple[str, list, list]:
    close_brackets_position = []
    open_brackets_position = []
    reverted_name = ""
    for idx, char in enumerate(text[::-1]):
        if char in open_brackets:
            reverted_name += close_brackets[open_brackets.index(char)]
            close_brackets_position.append(idx)
        elif char in close_brackets:
            reverted_name += open_brackets[close_brackets.index(char)]
            open_brackets_position.append(idx)
        else:
            reverted_name += char
    return reverted_name, open_brackets_position, close_brackets_position


class Tokenizer(Tokens):
    def __init__(self, filename: str, options: dict, keyword_manager: KeywordManager):
        self.filename = filename
        self.options = options
        delimiters = ''.join(
            ['\\' + d for d in self.options['allowed_delimiters']])
        self.pattern = '([{0}])'.format(delimiters)
        super().__init__(keyword_manager)

    @staticmethod
    def _get_brackets_position(filename) -> Tuple[str, list, list]:
        # find all brackets positions from self.filename
        open_brackets_position = []
        close_brackets_position = []
        for bracket in re.finditer(escaped_brackets, filename, re.IGNORECASE):
            if bracket.group() in open_brackets:
                open_brackets_position.append(bracket.start())
            else:
                close_brackets_position.append(bracket.start())

        # if the length is not same, then there is a bracket that is not closed or typo
        if len(open_brackets_position) != len(close_brackets_position):
            # if the different is even, then it is probably a typo
            if (len(open_brackets_position) - len(close_brackets_position)) % 2 == 0:
                all_bracket = sorted(open_brackets_position + close_brackets_position)
                last_seen = []
                expected = []
                reverted = False
                if len(close_brackets_position) > len(open_brackets_position):
                    # reverse the filename and invert open brackets and close brackets
                    reverted = True
                    filename, open_brackets_position, close_brackets_position = invert_string_brackets(
                        filename)
                    all_bracket = sorted(open_brackets_position + close_brackets_position)

                for index in all_bracket:
                    char = filename[index]
                    if char in open_brackets:
                        try:
                            abc = char == last_seen[-1]
                        except IndexError:
                            abc = False
                        if abc:
                            # We expected a close bracket, but we got the same open bracket
                            # This is probably a typo, replace it with correct bracket
                            corrected = close_brackets[open_brackets.index(char)]
                            filename = filename[:index] + corrected + filename[index + 1:]
                            # remove this index from open_brackets_position and add to close_brackets_position
                            open_brackets_position.remove(index)
                            close_brackets_position.append(index)
                            last_seen.pop()
                        else:
                            last_seen.append(char)
                            expected.append(close_brackets[open_brackets.index(char)])

                    else:
                        try:
                            if char == expected[-1]:
                                last_seen.pop()
                                expected.pop()
                        except IndexError:
                            pass
                if reverted:
                    filename, open_brackets_position, close_brackets_position = invert_string_brackets(
                        filename)

            # else: I'm not sure what to do here. Let's just ignore it and put on log
            else:
                logger.debug(f"Invalid brackets in {filename}")
                # if the length not same, if there's a same bracket next to each other, remove one of them
                if len(open_brackets_position) != len(close_brackets_position):
                    filename = re.sub(f"({'|'.join(escaped_open_brackets)})\\1+", "\\1", filename)
                    filename = re.sub(f"({'|'.join(escaped_close_brackets)})\\1+", "\\1", filename)
                    open_brackets_position = []
                    close_brackets_position = []
                    for bracket in re.finditer(escaped_brackets, filename, re.IGNORECASE):
                        if bracket.group() in open_brackets:
                            open_brackets_position.append(bracket.start())
                        else:
                            close_brackets_position.append(bracket.start())

        # just to make sure that the brackets are sorted
        open_brackets_position.sort()
        close_brackets_position.sort()
        return filename, open_brackets_position, close_brackets_position

    def _tokenize_by_brackets(self, filename) -> str:
        filename, open_brackets_position, close_brackets_position = self._get_brackets_position(filename)

        cursor = 0
        last_pair_index = 0
        for open_bracket_index in open_brackets_position:
            if open_bracket_index < cursor:
                continue

            if open_bracket_index != cursor:
                # Found a token before the bracket
                self._tokenize_by_pre_identified(
                    filename[cursor:open_bracket_index],
                    enclosed=False
                )
                cursor = open_bracket_index
            for last_pair_index, close_bracket_index in enumerate(close_brackets_position[last_pair_index:]):
                if (close_bracket_index > open_bracket_index
                        and filename[close_bracket_index] == close_brackets[open_brackets.index(
                            filename[open_bracket_index])]):
                    break
            else:
                close_bracket_index = -1
            if close_bracket_index == -1:
                self._tokenize_by_pre_identified(
                    filename[cursor:],
                    enclosed=False
                )
                cursor = len(filename)
            else:
                self._add_token(
                    TokenCategory.BRACKET, filename[open_bracket_index], enclosed=True,
                    element=ElementCategory.BRACKET)
                self._tokenize_by_pre_identified(
                    filename[cursor + 1:close_bracket_index],
                    enclosed=True
                )
                self._add_token(
                    TokenCategory.BRACKET, filename[close_bracket_index], enclosed=True,
                    element=ElementCategory.BRACKET)
                cursor = close_bracket_index + 1
        else:
            self._tokenize_by_pre_identified(
                filename[cursor:],
                enclosed=False
            )
        return filename

    def _tokenize_by_pre_identified(self, text, enclosed) -> None:
        if not text:
            return

        pre_identified_tokens = self.keyword_manager.peek(text)

        last_token_end_pos = 0
        for token_begin_pos, token_end_pos, category in pre_identified_tokens:
            if last_token_end_pos != token_begin_pos:
                # Tokenize the text between the pre-identified tokens
                self._tokenize_by_delimiters(
                    text[last_token_end_pos:token_begin_pos], enclosed)
            self._add_token(TokenCategory.IDENTIFIER, text[token_begin_pos:token_end_pos], enclosed,
                            category)
            last_token_end_pos = token_end_pos

        if last_token_end_pos != len(text):
            # Tokenize the text after the pre-identified tokens (or all the text
            # if there was no pre-identified tokens)
            self._tokenize_by_delimiters(text[last_token_end_pos:], enclosed)

    def _tokenize_by_delimiters(self, text, enclosed) -> None:
        splited_text = re.split(self.pattern, text)
        new_tokens = Tokens(self.keyword_manager)  # Create a new Tokens object to store the new tokens
        for sub_text in splited_text:
            if sub_text:
                if sub_text in self.options['allowed_delimiters']:
                    new_tokens._add_token(TokenCategory.DELIMITER, sub_text, enclosed, ElementCategory.DELIMITER)
                else:
                    stripped = sub_text.strip(f" {parser_helper.DASHES}")
                    # e.g S01E01- > S01E01
                    match = re.match(f"(.*)({re.escape(stripped)})(.*)", sub_text)
                    if match:
                        if match.group(1):
                            # "-" in "- " or "-Flac"
                            new_tokens._add_token(TokenCategory.UNKNOWN, match.group(1), enclosed)
                        if match.group(2):
                            new_tokens._add_token(TokenCategory.UNKNOWN, match.group(2), enclosed)
                        if match.group(3):
                            # "-" in "S01E01-"
                            new_tokens._add_token(TokenCategory.UNKNOWN, match.group(3), enclosed)

        new_tokens._validate_delimiter_tokens()

        self.add_list(new_tokens.tokens)

    def tokenize(self) -> bool:
        self.filename = self._tokenize_by_brackets(self.filename)
        return not self.empty()
