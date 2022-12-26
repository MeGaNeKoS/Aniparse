import itertools
import logging
import re
from typing import List, Tuple

from aniparse import constant, helper
from aniparse.element import ElementCategory
from aniparse.keyword_manager import KeywordManager
from aniparse.token import Tokens, TokenType, Token

logger = logging.getLogger(__name__)


class DelimiterTokens(Tokens):
    """
    A class representing a doubly linked list of `Token` objects that are created by
        the `tokenize_by_delimiter` method.
    This class provides methods for validating the tokens to ensure that certain tokens are not split improperly
        by the `tokenize_by_delimiter` method.
    For example, if the `tokenize_by_delimiter` method splits a token like "5.1" into two tokens "5" and "1",
    the validation methods in this class can identify and concatenate the two tokens back into a single "5.1" token.

    Note: This class is designed to handle the default allowed delimiters: " _.&+,|".
    If you have specified different delimiters in your options, you may need to create your own version
    of this class to handle the validation for those delimiters.
    """

    def __init__(self):
        """
        Initialize a new `DelimiterTokens` object.

        This method sets up the default values and placeholders for the tokens that will be removed later on
            in the validation process.
        """
        super().__init__()
        self.remove_buffer = []

    @staticmethod
    def is_delimiter_token(target_token: Token) -> bool:
        """
        Check if the given `Token` object is a delimiter token.

        Args:
        - target_token (Token): The `Token` object to check.

        Returns:
        - bool: True if the `Token` object is a delimiter token, False otherwise.
        """
        return (target_token is not None and
                target_token.type == TokenType.DELIMITER)

    @staticmethod
    def is_unknown_token(target_token: Token) -> bool:
        """
        Check if a given `Token` object is an unknown token.

        Args:
            target_token (Token): The `Token` object to check.

        Returns:
            bool: True if the `Token` object is an unknown token, False otherwise.
        """
        return (target_token is not None and
                target_token.type == TokenType.UNKNOWN)

    @classmethod
    def is_single_character_token(cls, target_token: Token) -> bool:
        """
        Check whether a token is an unknown token that contains only a single character.
        The single character must not be a dashes' character.

        Args:
        - target_token (Token): The token to check.

        Returns:
        - bool: True if the token is a single character unknown token, False otherwise.
        """
        return (cls.is_unknown_token(target_token) and
                len(target_token.content) == 1 and
                target_token.content not in constant.DASHES)

    def append_token_to(self, target_token, destination_token):
        """
        Append the content of `target_token` to `destination_token` and buffer `target_token` for later removal.

        This method is used to concatenate `Token` objects that were split by the delimiter tokenizing process.
        When concatenating tokens, we need to be careful not to remove them from the list before validation.
        If we remove a token before validation, it can cause issues with the token's position
            and the previous/next tokens.
        Therefore, we buffer the token for later removal after the validation process has completed.

        Example:
            Suppose we have the following list of tokens: '[5', '.', '1', '+', '2', '.', '0]']
            If we concatenate and remove `target_token` (e.g. `'.'`) from the list as we go, the list becomes:
                '[5.1+2', '.', '0]']
            From the perspective of the token at index 5 (`'.'`), its previous token becomes '[5.1+2'.
            This means that the previous token does not satisfy the condition for being a single character token,
                and the validation process fails.
            To avoid this, we buffer `target_token` and remove it from the list after the validation process.
            This allows us to retain the original list of tokens and ensures
                that the validation process is performed correctly.

        Args:
            target_token (Token): The `Token` object whose content will be appended to `destination_token`.
            destination_token (Token): The `Token` object that will have the content of `target_token` appended to it.
        """
        destination_token.content += target_token.content
        if target_token not in self.remove_buffer:
            self.remove_buffer.append(target_token)

    def validate_delimiter_tokens(self) -> None:
        """
        Validate the delimiter tokens by concatenating them with their surrounding unknown tokens as needed.
        This method is designed to handle cases where delimiter tokens in " _.&+,|" have caused unwanted splits
        in the token list during tokenization. It checks for various conditions, such as single character unknown
        tokens on either side of a delimiter, or consecutive delimiter tokens with different characters, and
        combines them as necessary.

        This method iterates through the `DelimiterTokens` list and checks for certain cases where
        delimiter tokens should be combined with adjacent tokens.
        For example, if the list contains the tokens "[5", ".", "1]" and the delimiter is ".",
        this method will combine these tokens into a single token "[5.1]".

        Note: If the user has allowed delimiters that are not included in the default set of " _.&+,|",
        this method may not be sufficient and a custom implementation may be needed.

        Returns:
            None: This method modifies the token list in place and does not return anything.
        """
        for token in self.loop_forward():
            if token.type != TokenType.DELIMITER:
                continue

            delimiter = token.content
            if delimiter == ",":
                continue

            prev_token = token.prev
            next_token = token.next

            if delimiter not in ' _':
                if self.is_single_character_token(prev_token):
                    self.append_token_to(token, prev_token)
                    while self.is_unknown_token(next_token):
                        self.append_token_to(next_token, prev_token)
                        next_token = next_token.next

                        if (self.is_delimiter_token(next_token) and
                                next_token.content == delimiter):
                            pass
                    # end of loop
                    token.next = next_token
                    continue

                if self.is_single_character_token(next_token):
                    # e.g. "." in "07.1", "." in "TrueHD5.1"
                    self.append_token_to(token, prev_token)
                    self.append_token_to(next_token, prev_token)
                    # remove next token from the chain
                    if next_token.next:
                        next_token.next.prev = prev_token
                    token.next = next_token.next
                    continue

            # Chrono Crusade ep. 1-5
            if (self.is_unknown_token(prev_token) and
                    self.is_delimiter_token(next_token)):

                next_delimiter = next_token.content
                if delimiter != next_delimiter and delimiter != ',':
                    if next_delimiter == ' ' or next_delimiter == '_':
                        self.append_token_to(token, prev_token)
                        continue

            elif (self.is_delimiter_token(prev_token) and
                  self.is_delimiter_token(next_token)):

                prev_delimiter = prev_token.content
                next_delimiter = next_token.content
                if (prev_delimiter == next_delimiter and
                        prev_delimiter != delimiter):
                    # e.g. "&" in "_&_"
                    token.type = TokenType.UNKNOWN
                    token.element = ElementCategory.UNKNOWN

            # Check for other special cases (01+02)
            if delimiter in '+&':
                if (self.is_unknown_token(prev_token) and
                        self.is_unknown_token(next_token)):

                    # if both token are digits, then it's a range
                    if (helper.is_number(prev_token.content) and
                            helper.is_number(next_token.content)):
                        self.append_token_to(token, prev_token)
                        self.append_token_to(next_token, prev_token)  # e.g. "01+02"

        for token in reversed(self.remove_buffer):
            self.remove(token)


class Tokenizer:
    """
    A class for tokenizing filenames.

    The `Tokenizer` class is responsible for breaking down a given filename string into a list of individual
    `Token` objects, which can then be processed and validated by other parts of the library.
    It does this by first tokenizing the string by brackets, then by pre-identifier keywords from a `KeywordManager`
    object, and finally by delimiters.
    """

    find_brackets = re.compile(constant.BRACKET_PATTERN, flags=re.IGNORECASE)

    def __init__(self, filename: str, delimiters: str, keyword_manager: KeywordManager):
        """
        Initialize a Tokenizer object.

        Args:
            filename (str): The string representing the filename to be tokenized.
            delimiters (str): A string containing the characters to use as delimiters for tokenization.
            keyword_manager (KeywordManager): A KeywordManager object containing the keywords to use for tokenization.
        """
        self.filename = filename
        self.keyword_manager = keyword_manager
        self.delimiters = delimiters
        self.tokens = Tokens()

        self._delimiter_regex = re.compile(f"({'|'.join(map(re.escape, delimiters))})",
                                           flags=re.IGNORECASE)

    @staticmethod
    def check_bracket_balance(open_brackets_positions: list, close_brackets_positions: list) -> bool:
        """
        Check whether the brackets in a string are balanced or not.

        Parameters:
        open_brackets_positions (list): A list of indices of open brackets in the string.
        close_brackets_positions (list): A list of indices of close brackets in the string.

        Returns:
        bool: True if the brackets are balanced, False otherwise.
        """
        if len(open_brackets_positions) != len(close_brackets_positions):
            return False
        else:
            for (open_brackets_position,
                 close_brackets_position) in zip(open_brackets_positions,
                                                 close_brackets_positions):
                if open_brackets_position > close_brackets_position:
                    return False

        return True

    @staticmethod
    def invert_string_brackets(text: str, open_bracket_positions: List[int],
                               close_bracket_position: List[int]) -> Tuple[str, List[int], List[int]]:
        """
        Invert the brackets in a string and return the inverted string along with the positions of
        the open and close brackets.

        Parameters:
        - text (str): The string to invert the brackets in.
        - open_bracket_positions (List[int]): A list of integers representing the indices of the open brackets
            in the original string.
        - close_bracket_position (List[int]): A list of integers representing the indices of the close brackets
            in the original string.

        Returns:
        - A tuple containing:
            - The inverted string.
            - A list of integers representing the indices of the open brackets in the inverted string.
            - A list of integers representing the indices of the close brackets in the inverted string.
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

        Args:
            string (str): The string to search for brackets.

        Returns:
            tuple: A tuple containing two lists, the first list representing the positions of
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
                                close_brackets_position: List[int]) -> str:
        """
        Fixes unbalanced brackets in the given filename.

        This method attempts to fix unbalanced brackets in the given filename by identifying and correcting any
        typos or mistakes made in the placement of brackets.

        If the number of open and close brackets is not equal, the method will try to fix the imbalance
        by identifying and correcting any typos or mistakes in the placement of brackets.

        If the imbalance cannot be corrected, the method will log the issue and
        replace any multiple same brackets next to each other with a single bracket.

        Parameters:
        - filename: str
            The filename to fix.
        - open_brackets_position: List[int]
            A list of indices of open brackets in the given filename.
        - close_brackets_position: List[int]
            A list of indices of close brackets in the given filename.

        Returns:
        - str
            The fixed filename.
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

        return filename

    def _tokenize_by_brackets(self) -> None:
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

        Returns:
            None: This method modifies the `tokens` attribute of the `Tokenizer` object in place and does not return
                anything.
        """
        open_brackets_position, close_brackets_position = self.find_all_brackets(self.filename)

        # if the length is not same, then there is a bracket that is not closed or typo
        if not self.check_bracket_balance(open_brackets_position, close_brackets_position):
            self.filename = self.fix_unbalanced_brackets(self.filename, open_brackets_position, close_brackets_position)
            open_brackets_position, close_brackets_position = self.find_all_brackets(self.filename)

        cursor = 0
        last_pair_index = 0
        for open_bracket_index, next_open_bracket_index in zip(open_brackets_position,
                                                               itertools.chain(
                                                                   open_brackets_position[1:],
                                                                   [len(self.filename) + 1])
                                                               ):
            if open_bracket_index < cursor:
                continue

            if open_bracket_index != cursor:
                # Found a token before the bracket
                self._tokenize_by_pre_identifier(
                    self.filename[cursor:open_bracket_index],
                    enclosed=False
                )
                cursor = open_bracket_index

            for last_pair_index, close_bracket_index in enumerate(close_brackets_position[last_pair_index:]):
                if (open_bracket_index < close_bracket_index < next_open_bracket_index
                        and self.filename[close_bracket_index] == constant.CLOSE_BRACKETS[constant.OPEN_BRACKETS.index(
                            self.filename[open_bracket_index])]):
                    break
            else:
                close_bracket_index = -1

            if close_bracket_index == -1:
                self._tokenize_by_pre_identifier(
                    self.filename[cursor:],
                    enclosed=False
                )
                cursor = len(self.filename)
            else:
                self.tokens.append(Token(
                    self.filename[open_bracket_index], TokenType.BRACKET,
                    ElementCategory.BRACKET, enclosed=True))
                self._tokenize_by_pre_identifier(
                    self.filename[cursor + 1:close_bracket_index],
                    enclosed=True
                )
                self.tokens.append(
                    Token(self.filename[close_bracket_index], TokenType.BRACKET,
                          ElementCategory.BRACKET, enclosed=True))
                cursor = close_bracket_index + 1
        else:
            self._tokenize_by_pre_identifier(
                self.filename[cursor:],
                enclosed=False
            )

    def _tokenize_by_pre_identifier(self, text: str, enclosed: bool) -> None:
        """
        Tokenize the given text by pre-identified tokens.

        Args:
            text (str): The text to tokenize.
            enclosed (bool): Whether the text is enclosed within brackets.

        Returns:
            None
        """
        if not text:
            return

        pre_identified_tokens = self.keyword_manager.pre_identify_tokens(text)

        start_pos = 0
        for token_start, token_end, category in pre_identified_tokens:
            # Tokenize the substring before the pre-identified token
            if start_pos < token_start:
                self._tokenize_by_delimiter(text[start_pos:token_start], enclosed)

            # Add the pre-identified token
            self.tokens.append(Token(text[token_start:token_end], TokenType.IDENTIFIER, category, enclosed))

            # Update the start position for the next iteration
            start_pos = token_end

        # Tokenize the substring after the last pre-identified token
        if start_pos < len(text):
            self._tokenize_by_delimiter(text[start_pos:], enclosed)

    def _tokenize_by_delimiter(self, text: str, enclosed: bool) -> None:
        """
        Tokenize the given text by the delimiters specified in the options.

        Args:
        - text (str): The text to tokenize
        - enclosed (bool): Whether the text is enclosed within brackets or not.
          This determines whether the delimiters are treated as brackets or not.

        Returns:
        - None
        """
        if not text:
            return

        delimiter_tokens = DelimiterTokens()
        # Iterate through the tokens and create Token objects
        for sub_text in self._delimiter_regex.split(text):
            if not sub_text:
                continue

            if sub_text in self.delimiters:
                delimiter_tokens.append(
                    Token(sub_text, TokenType.DELIMITER, ElementCategory.DELIMITER)
                )
            else:
                stripped = sub_text.strip(f" {constant.DASHES}")
                if sub_text != stripped:
                    # e.g S01E01- > S01E01
                    match = re.match(f"(.*)({re.escape(stripped)})(.*)", sub_text)
                    if match:
                        if match.group(1):
                            # "-" in "- " or "-Flac"
                            delimiter_tokens.append(
                                Token(match.group(1), enclosed=enclosed)
                            )
                        if match.group(2):
                            delimiter_tokens.append(
                                Token(match.group(2), enclosed=enclosed)
                            )
                        if match.group(3):
                            # "-" in "S01E01-"
                            delimiter_tokens.append(
                                Token(match.group(3), enclosed=enclosed)
                            )
                else:
                    delimiter_tokens.append(
                        Token(sub_text, enclosed=enclosed)
                    )

        delimiter_tokens.validate_delimiter_tokens()
        self.tokens.extend(delimiter_tokens)

    def tokenize(self) -> Tokens:
        """
        Tokenize the filename provided to the Tokenizer object.

        This method tokenizes the filename by first identifying any brackets and tokenizing them separately.
        It then tokenizes the remaining string using delimiter tokens and pre-identifier keywords.

        Returns:
            Tokens: A list of Token objects representing the tokenized version of the filename.
        """
        self._tokenize_by_brackets()
        return self.tokens
