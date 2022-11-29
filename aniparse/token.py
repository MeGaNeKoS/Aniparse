from enum import Enum
from typing import List, Union

from aniparse.element import ElementCategory
from aniparse.keyword import KeywordManager


class TokenCategory(Enum):
    # Auto enumerate elements
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    UNKNOWN = ()
    BRACKET = ()
    DELIMITER = ()
    IDENTIFIER = ()
    INVALID = ()


class TokenFlags(int):
    NONE = 0
    # Categories
    BRACKET = 1 << 0
    NOT_BRACKET = 1 << 1
    DELIMITER = 1 << 2
    NOT_DELIMITER = 1 << 3
    IDENTIFIER = 1 << 4
    NOT_IDENTIFIER = 1 << 5
    UNKNOWN = 1 << 6
    NOT_UNKNOWN = 1 << 7
    VALID = 1 << 8
    NOT_VALID = 1 << 9
    # Enclosed
    ENCLOSED = 1 << 10
    NOT_ENCLOSED = 1 << 11
    # Masks
    MASK_CATEGORIES = (
            BRACKET | NOT_BRACKET |
            DELIMITER | NOT_DELIMITER |
            IDENTIFIER | NOT_IDENTIFIER |
            UNKNOWN | NOT_UNKNOWN |
            VALID | NOT_VALID
    )
    MASK_ENCLOSED = ENCLOSED | NOT_ENCLOSED


class Token:
    def __init__(self, content: str = None, t_category: TokenCategory = TokenCategory.UNKNOWN,
                 e_category: ElementCategory = ElementCategory.UNKNOWN, enclosed: bool = False):
        self.t_category = t_category
        self.content = content
        self.enclosed = enclosed
        self.e_category = e_category

    def __repr__(self):
        return (f"Token(content = \"{self.content}\", category = {self.t_category}, "
                f"element = {self.e_category}), enclosed = {self.enclosed}")

    def check_elements(self, elements: ElementCategory = None):
        if elements:
            return self.e_category in elements
        return True

    # check if token is of a certain category
    def check_flags(self, flags: int = None):
        # Checking for flags is set for this token
        # e.g. if we're looking key with flags IDENTIFIER,
        # we compare the flags binary with the token's flags binary
        # and check if the IDENTIFIER bit is set
        if flags is None:
            return True

        # local function to check if a flag is equal
        def check_flag(flag: int):
            return (flags & flag) == flag

        # if MASK_ENCLOSED is set, check if enclosed is equal to the flag
        if flags & TokenFlags.MASK_ENCLOSED:
            if not check_flag(TokenFlags.ENCLOSED if self.enclosed else TokenFlags.NOT_ENCLOSED):
                return False

        # if MASK_CATEGORIES is set, check if category is equal to the flag
        if flags & TokenFlags.MASK_CATEGORIES:
            if check_flag(TokenFlags.BRACKET
                          if self.t_category == TokenCategory.BRACKET else TokenFlags.NOT_BRACKET):
                return True
            if check_flag(TokenFlags.DELIMITER
                          if self.t_category == TokenCategory.DELIMITER else TokenFlags.NOT_DELIMITER):
                return True
            if check_flag(TokenFlags.IDENTIFIER
                          if self.t_category == TokenCategory.IDENTIFIER else TokenFlags.NOT_IDENTIFIER):
                return True
            if check_flag(TokenFlags.UNKNOWN
                          if self.t_category == TokenCategory.UNKNOWN else TokenFlags.NOT_UNKNOWN):
                return True
            if check_flag(TokenFlags.VALID
                          if self.t_category != TokenCategory.INVALID else TokenFlags.NOT_VALID):
                return True
            return False
        return True


class Tokens:
    def __init__(self, keyword_manager: KeywordManager):
        self.tokens = []  # type: List[Token]
        self.counter = {}  # type: (ElementCategory, int)
        self.keyword_manager = keyword_manager

    def _add_token(self, category, content, enclosed, element=ElementCategory.UNKNOWN) -> Token:
        new_token = Token(content, category, element, enclosed)
        self.append(new_token)
        return new_token

    def _validate_delimiter_tokens(self) -> None:
        removed = {}

        def find_previous_valid_token(target_token) -> Token:
            return self.find_prev(target_token, TokenFlags.VALID)

        def find_next_valid_token(target_token) -> Token:
            return self.find_next(target_token, TokenFlags.VALID)

        def is_delimiter_token(target_token) -> bool:
            return target_token is not None and \
                   target_token.t_category == TokenCategory.DELIMITER

        def is_unknown_token(target_token) -> bool:
            return target_token is not None and \
                   target_token.t_category == TokenCategory.UNKNOWN

        def is_single_character_token(target_token) -> bool:
            return is_unknown_token(target_token) and len(target_token.content) == 1 and \
                   target_token.content != '-'

        def append_token_to(target_token, append_to) -> None:
            if target_token in removed:
                return
            if append_to in removed:
                append_to = removed[append_to]
            append_to.content += target_token.content
            # remove this token
            removed[target_token] = append_to

        for token in self.get_list():

            if token.t_category != TokenCategory.DELIMITER:
                continue

            delimiter = token.content
            if delimiter == ",":
                continue
            prev_token = find_previous_valid_token(token)
            next_token = find_next_valid_token(token)

            # Check for single-character tokens to prevent splitting group
            # names, keywords, episode number, etc.
            # come back later
            if delimiter != ' ' and delimiter != '_':
                if is_single_character_token(prev_token):
                    append_token_to(token, prev_token)
                    while is_unknown_token(next_token):

                        # 2nd "." in "R.O.D"
                        append_token_to(next_token, prev_token)
                        next_token = find_next_valid_token(next_token)
                        if is_delimiter_token(next_token) and \
                                next_token.content == delimiter:
                            # "." in "R.O."
                            append_token_to(next_token, prev_token)
                            next_token = find_next_valid_token(next_token)
                    continue
                if is_single_character_token(next_token):
                    # e.g. "." in "07.1", "." in "TrueHD5.1"
                    append_token_to(token, prev_token)
                    append_token_to(next_token, prev_token)
                    continue

            # Check for adjacent delimiters
            if is_unknown_token(prev_token) and is_delimiter_token(next_token):
                next_delimiter = next_token.content
                if delimiter != next_delimiter and delimiter != ',':
                    if next_delimiter == ' ' or next_delimiter == '_':
                        append_token_to(token, prev_token)  # e.g. "." in "Vol. ", "Ep. "

            elif is_delimiter_token(prev_token) and \
                    is_delimiter_token(next_token):
                prev_delimiter = prev_token.content
                next_delimiter = next_token.content
                if prev_delimiter == next_delimiter and \
                        prev_delimiter != delimiter:
                    self.set_token_element(token, TokenCategory.UNKNOWN, ElementCategory.UNKNOWN)  # e.g. "&" in "_&_"

            # Check for other special cases
            if delimiter == '&' or delimiter == '+':
                if is_unknown_token(prev_token) and \
                        is_unknown_token(next_token):
                    if prev_token.content.isdigit() and \
                            next_token.content.isdigit():
                        append_token_to(token, prev_token)
                        append_token_to(next_token, prev_token)  # e.g. "01+02"

        for token in removed:
            self.remove_token(token)

    def append(self, token: Token) -> None:
        self.tokens.append(token)
        self.counter[token.e_category] = self.counter.get(token.e_category, 0) + 1

    def add_list(self, tokens: List[Token]) -> None:
        for token in tokens:
            self.append(token)

    def distance(self, token1: Token = None, token2: Token = None) -> int:
        begin_index = 0 if token1 is None else self.get_index(token1)
        end_index = len(self.tokens) if token2 is None else self.get_index(token2)
        return abs(end_index - begin_index)

    def empty(self) -> bool:
        return len(self.tokens) == 0

    def find(self, flags: int) -> Token:
        return self.find_in_tokens(self.tokens, flags)

    @staticmethod
    def find_in_tokens(tokens: List[Token],
                       flags: int,
                       elements: Union[ElementCategory, List[ElementCategory]] = None
                       ) -> Union[Token, None]:
        # return the first token that matches the flags
        for token in tokens:
            if not token.check_elements(elements):
                continue
            if token.check_flags(flags):
                return token
        return None

    def find_next(self, token: Token = None, flags: int = None, element: Union[ElementCategory, List[ElementCategory]] = None) -> Union[Token, None]:
        tokens = self.tokens
        if token is not None:
            tokens = tokens[self.get_index(token) + 1:]
        return self.find_in_tokens(tokens, flags, element)

    def find_prev(self, token: Token = None, flags: int = None, element: Union[ElementCategory, List[ElementCategory]] = None) -> Union[Token, None]:
        tokens = self.tokens.copy()  # make copy of the list, but the tokens are still the same
        if token is None:
            tokens.reverse()
        else:
            tokens = tokens[max(self.get_index(token) - 1, 0)::-1]
        return self.find_in_tokens(tokens, flags, element)

    def get(self, index: int) -> Token:
        return self.tokens[index]

    def get_index(self, token: Token) -> int:
        return self.tokens.index(token)

    def get_list(self,
                 flags: int = None,
                 begin: Token = None,
                 end: Token = None,
                 elements: Union[ElementCategory, List[ElementCategory]] = None) -> List[Token]:

        begin_index = 0 if begin is None else self.get_index(begin)
        end_index = len(self.tokens) if end is None else self.get_index(end)
        tokens = self.tokens[begin_index:end_index + 1]

        if elements:
            tokens = (token for token in tokens if token.check_elements(elements))

        if flags:
            tokens = (t for t in tokens if t.check_flags(flags))
        return tokens

    def insert(self, index: int, token: Token) -> None:
        self.tokens.insert(index, token)
        self.counter[token.e_category] = self.counter.get(token.e_category, 0) + 1

    def insert_after(self, token: Token, new_token: Token) -> None:
        self.insert(self.get_index(token) + 1, new_token)

    def insert_before(self, token: Token, new_token: Token) -> None:
        self.insert(self.get_index(token), new_token)

    def insert_tokens(self, token: Token, word: str, category: TokenCategory,
                      element: ElementCategory) -> Token:
        new_token = Token(word, category, element, token.enclosed)
        self.insert_after(token,
                          new_token
                          )
        return new_token

    def is_token_isolated(self, token: Token) -> bool:
        previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
        if previous_token.t_category != TokenCategory.BRACKET:
            return False

        next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
        if next_token.t_category != TokenCategory.BRACKET:
            return False
        return True

    def remove_token(self, token: Token) -> None:
        self.counter[token.e_category] -= 1
        self.tokens.remove(token)

    def set_token_element(self, token: Token, t_category: TokenCategory, e_category: ElementCategory) -> None:
        self.counter[token.e_category] -= 1
        self.counter[e_category] = self.counter.get(e_category, 0) + 1
        token.t_category = t_category
        token.e_category = e_category
