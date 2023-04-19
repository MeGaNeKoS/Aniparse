import itertools
import logging
import re
from typing import List, Tuple

from aniparse import constant
from aniparse.parser_option import Options
from aniparse.keyword import KeywordManager
from aniparse.element import ElementCategory
from aniparse.token import Tokens, TokenType, Token

logger = logging.getLogger(__name__)


class Tokenizer:
    """
    A class for tokenizing filenames.

    The `Tokenizer` class is responsible for breaking down a given filename string into a list of individual
    `Token` objects, which can then be processed and validated by other parts of the library.
    It does this by first tokenizing the string by brackets, then by pre-identifier keywords from a `KeywordManager`
    object, and finally by delimiters.
    """

    find_brackets = re.compile(constant.BRACKET_PATTERN, flags=re.IGNORECASE)

    def __init__(self, filename: str, options: Options, keyword_manager: KeywordManager):
        """
        Initialize a Tokenizer object.

        Parameters:
            filename (str): The string representing the filename to be tokenized.
            options (Options): An Options class for tokenizing.
            keyword_manager (KeywordManager): A KeywordManager class for tokenizing.
        """
        self.filename = filename
        self.tokens = Tokens()
        self.options = options
        self.keyword_manager = keyword_manager

    @staticmethod
    def is_bracket_unbalance(open_brackets_positions: list, close_brackets_positions: list) -> bool:
        """
        Check whether the brackets in a string are balanced or not.

        Parameters:
            open_brackets_positions (list): A list of indices of open brackets in the string.
            close_brackets_positions (list): A list of indices of close brackets in the string.

        Return:
            bool: True if the brackets are unbalanced, False otherwise.
        """
        if len(open_brackets_positions) != len(close_brackets_positions):
            return True

        # Text: This )is( )unbalance( text
        for open_brackets_position, close_brackets_position in zip(open_brackets_positions, close_brackets_positions):
            if open_brackets_position > close_brackets_position:
                return True

        return False

    @staticmethod
    def invert_string_brackets(text: str, open_bracket_positions: List[int],
                               close_bracket_position: List[int]) -> Tuple[str, List[int], List[int]]:
        """
        Invert the brackets in a string and return the inverted string along with the positions of
        the open and close brackets.

        Parameters:
            text (str): The string to invert the brackets in.
            open_bracket_positions (List[int]): A list of integers representing the indices of the open brackets
                in the original string.
            close_bracket_position (List[int]): A list of integers representing the indices of the close brackets
                in the original string.

        Returns:
            A tuple containing:
                The inverted string.
                A list of integers representing the indices of the open brackets in the inverted string.
                A list of integers representing the indices of the close brackets in the inverted string.
        """

        new_close_brackets_position = []
        new_open_brackets_position = []
        for index in open_bracket_positions:
            text = text[:index] + constant.CLOSE_BRACKETS[constant.OPEN_BRACKETS.index(text[index])] + text[index + 1:]
            new_close_brackets_position.insert(0, len(text) - index - 1)
        for index in close_bracket_position:
            text = text[:index] + constant.OPEN_BRACKETS[constant.CLOSE_BRACKETS.index(text[index])] + text[index + 1:]
            new_open_brackets_position.insert(0, len(text) - index - 1)

        return text[::-1], new_open_brackets_position, new_close_brackets_position

    @classmethod
    def find_all_brackets(cls, string: str) -> Tuple[List[int], List[int]]:
        """
        Find the positions of all brackets in a string.

        Parameters:
            string (str): The string to search for brackets.

        Returns:
            A tuple containing two lists, the first list representing the positions of
            open brackets in the string and the second list representing the positions of
            close brackets in the string.
        """
        open_brackets_position = []
        close_brackets_position = []
        for bracket in cls.find_brackets.finditer(string):
            if bracket.group() in constant.OPEN_BRACKETS:
                open_brackets_position.append(bracket.start())
            else:
                close_brackets_position.append(bracket.start())
        return open_brackets_position, close_brackets_position

    @classmethod
    def fix_unbalanced_brackets(cls, filename: str, open_brackets_position: List[int],
                                close_brackets_position: List[int], strict_mode: bool = False) -> str:
        """
        Fixes unbalanced brackets in the given filename.

        This method attempts to fix unbalanced brackets in the given filename by identifying and correcting any
        typos or mistakes made in the placement of brackets.

        If the number of open and close brackets is not equal, the method will try to fix the imbalance
        by identifying and correcting any typos or mistakes in the placement of brackets.

        If the imbalance cannot be corrected, the method will log the issue and
        replace any multiple same brackets next to each other with a single bracket.

        Parameters:
            filename (str): The filename to fix.
            open_brackets_position (List[int]): A list of indices of open brackets in the given filename.
            close_brackets_position (List[int]):A list of indices of close brackets in the given filename.
            strict_mode (bool): Whether to strict only process with balanced brackets.

        Return:
            The fixed filename as string.
        """
        if (len(open_brackets_position) - len(close_brackets_position)) % 2 == 0:
            all_bracket = sorted(open_brackets_position + close_brackets_position)
            last_seen = []
            expected = []
            reverted = False
            if len(close_brackets_position) > len(open_brackets_position):
                # reverse the filename and invert open brackets and close brackets
                reverted = True
                filename, open_brackets_position, close_brackets_position = cls.invert_string_brackets(
                    filename, open_brackets_position, close_brackets_position)
                all_bracket = sorted(open_brackets_position + close_brackets_position)

            for index in all_bracket:
                char = filename[index]
                if char in constant.OPEN_BRACKETS:
                    try:
                        expected_char = char == last_seen[-1]
                    except IndexError:
                        expected_char = False
                    if expected_char:
                        # We expected a close bracket, but we got the same open bracket
                        # This is probably a typo, replace it with correct bracket
                        corrected = constant.CLOSE_BRACKETS[constant.OPEN_BRACKETS.index(char)]
                        filename = filename[:index] + corrected + filename[index + 1:]
                        # remove this index from open_brackets_position and add to close_brackets_position
                        open_brackets_position.remove(index)
                        close_brackets_position.append(index)
                        last_seen.pop()
                    else:
                        last_seen.append(char)
                        expected.append(constant.CLOSE_BRACKETS[constant.OPEN_BRACKETS.index(char)])

                else:
                    try:
                        if char == expected[-1]:
                            last_seen.pop()
                            expected.pop()
                    except IndexError:
                        pass
            if reverted:
                filename, open_brackets_position, close_brackets_position = cls.invert_string_brackets(
                    filename, open_brackets_position, close_brackets_position)

            # if (len(open_brackets_position) - len(close_brackets_position)) % 2 == 0:
        else:
            # else: I'm not sure what to do here. Let's just ignore it and put on log
            logger.debug(f"Invalid brackets in {filename}")
            # if the length not same, if there's a same bracket next to each other, remove one of them
            if len(open_brackets_position) != len(close_brackets_position):
                filename = re.sub(f"({constant.OPEN_BRACKETS_PATTERN})\\1+", "\\1", filename)
                filename = re.sub(f"({constant.CLOSE_BRACKETS_PATTERN})\\1+", "\\1", filename)
            elif strict_mode:
                raise ValueError(f"Invalid brackets in {filename}")
        return filename

    def _tokenize_by_brackets(self, filename: str = None, nested_level: int = 0) -> None:
        """
        Tokenize the filename by identifying and processing bracket tokens.

        This method iterates through the `filename` string and uses the `find_all_brackets` method to locate
        all open and close brackets in the string. It then checks whether the brackets are balanced and, if not,
        uses the `fix_unbalanced_brackets` method to try and correct any errors or typos.

        Once all brackets have been identified, this method iterates through the list of open bracket positions and
        attempts to find the corresponding close bracket for each open bracket. If a close bracket is found, the
        method creates `BRACKET` tokens for both the open and close brackets and processes the string between them
        using the `_tokenize_by_pre_identifier` method. If no close bracket is found, the rest of the `filename`
        string is processed as a regular token.

        Parameters:
            filename (str): The filename to tokenize. If not provided, the `filename` attribute of the `Tokenizer`
                object is used.
            nested_level (int): The nested level of the current filename. This is used to keep track of the
                nested level of the current filename and is used to determine the `nested_level` attribute of
                the `BRACKET` tokens.
        Return:
            None: This method modifies the `tokens` attribute of the `Tokenizer` object in place and does not return
                anything.
        """
        if not filename:
            filename = self.filename

        open_brackets_position, close_brackets_position = self.find_all_brackets(filename)

        # if the length is not same, then there is a bracket that is not closed or typo
        if self.is_bracket_unbalance(open_brackets_position, close_brackets_position):
            filename = self.fix_unbalanced_brackets(filename, open_brackets_position, close_brackets_position,
                                                    self.options.strict)
            open_brackets_position, close_brackets_position = self.find_all_brackets(filename)

        cursor = 0  # THe bracket index in the filename
        last_pair_index = 0  # The bracket index in the list

        open_brackets_position.append(len(filename) + 1)
        for open_bracket_index, next_open_bracket_index in zip(open_brackets_position[:-1],
                                                               itertools.chain(open_brackets_position[1:])):
            if open_bracket_index < cursor:
                continue

            if open_bracket_index != cursor:
                # Found a token before the bracket
                self._tokenize_by_delimiter(
                    filename[cursor:open_bracket_index],
                    nest_level=nested_level
                )
                cursor = open_bracket_index

            # Find the root close bracket pair
            close_bracket_skipped = 0
            have_nested = False
            for last_pair_index, close_bracket_index in enumerate(close_brackets_position[last_pair_index:]):
                if close_bracket_skipped > 1:
                    close_bracket_skipped -= 1
                    continue
                elif close_bracket_skipped == 1:
                    close_bracket_skipped = 0

                if close_bracket_index > next_open_bracket_index:
                    have_nested = True
                    # Intentional overwrite `next_open_bracket_index`
                    for next_open_bracket_index in open_brackets_position[last_pair_index + 1:]:  # noqa
                        if next_open_bracket_index < close_bracket_index:
                            close_bracket_skipped += 1
                        else:
                            break

                if (close_bracket_skipped == 0 and
                        open_bracket_index < close_bracket_index and
                        filename[close_bracket_index] == constant.CLOSE_BRACKETS[
                            constant.OPEN_BRACKETS.index(filename[open_bracket_index])
                        ]):
                    break
            else:
                close_bracket_index = -1

            if close_bracket_index == -1:
                self._tokenize_by_delimiter(
                    filename[cursor:],
                    nest_level=nested_level
                )
                cursor = len(filename)
            else:
                self.tokens.add_token(Token(
                    filename[open_bracket_index], TokenType.BRACKET,
                    ElementCategory.BRACKET, nest_level=nested_level))
                # This loop will tokenize based on bracket. But it only counts the root bracket,
                # nested bracket will be count as content of the root bracket.
                if have_nested:
                    self._tokenize_by_brackets(filename[cursor + 1:close_bracket_index], nested_level + 1)
                else:
                    self._tokenize_by_delimiter(
                        filename[cursor + 1:close_bracket_index],
                        nest_level=nested_level + 1
                    )
                self.tokens.add_token(
                    Token(filename[close_bracket_index], TokenType.BRACKET,
                          ElementCategory.BRACKET, nest_level=nested_level))
                cursor = close_bracket_index + 1
        else:
            self._tokenize_by_delimiter(
                filename[cursor:],
                nest_level=nested_level
            )

    def _tokenize_by_delimiter(self, text: str, nest_level: int) -> None:
        """
        Tokenize the given text by the delimiters specified in the options.

        Parameters:
            text (str): The text to tokenize
            nest_level (int): The nested level of the current filename part. This is used to keep track of the
                nested level of the current filename and is used to determine the `nested_level` attribute of
                the `BRACKET` tokens.

        Return:
            None: This method modifies the `tokens` attribute of the `Tokenizer` object in place and does not return
        """
        if not text:
            return

        # Iterate through the tokens and create Token objects
        for sub_text in self.options.delimiter_regex.split(text):
            if not sub_text:
                continue

            if (sub_text in self.options.allowed_delimiter and
                    # This character not part of range_separator
                    sub_text not in constant.RANGE_SEPARATOR):
                self.tokens.add_token(Token(content=sub_text,
                                            type_=TokenType.DELIMITER,
                                            category=ElementCategory.DELIMITER,
                                            nest_level=nest_level))
                continue

            self.tokens.add_token(Token(sub_text, nest_level=nest_level))

    def tokenize(self) -> Tokens:
        """
        Tokenize the filename provided to the Tokenizer object.

        This method tokenizes the filename by first identifying any brackets and tokenizing them separately.
        It then tokenizes the remaining string using delimiter tokens.

        Returns:
            Tokens: A list of Token objects representing the tokenized version of the filename.
        """
        self._tokenize_by_brackets()
        return self.tokens
