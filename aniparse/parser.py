import re
from typing import Tuple, Union

from aniparse import constant
from aniparse.keyword import Keyword, KeywordManager
from aniparse.parser_option import Options
from aniparse.element import ElementCategory

from aniparse.token import TokenType, Token
from aniparse.tokenizer import Tokenizer


# TODO: Refactor this class
def get_number_from_ordinal(string: str):
    return constant.ORDINALS.get(string.lower())


def is_dash(token: Token) -> bool:
    return token and token.content in constant.DASHES


def is_delimiter(token: Token) -> bool:
    return token and token.type == TokenType.DELIMITER


def is_context_delimiter(token: Token) -> bool:
    return token and token.content in constant.DASHES


def is_range(token: Token) -> bool:
    return token and token.content in constant.RANGE_SEPARATOR


def is_resolution(string) -> bool:
    return bool(re.match(r'\d{3,4}([ip]|([x\u00D7]\d{3,4}))$', string, flags=re.IGNORECASE))


def is_bracket(word):
    return word in constant.BRACKETS


def set_token(token: Token, type_: TokenType, category: ElementCategory):
    token.type = type_
    token.category = category
    token.remove_possibility()
    token.add_possibility(category)


class BaseParser:
    def __init__(self, filename: str, options: Options, keyword_manager: KeywordManager):
        """
        Initialize a Parser object.

        Args:
            filename (str): The string representing the filename to be parsed.
            options (Options): An Options class for parsing.
            keyword_manager (KeywordManager): A KeywordManager class for parsing.
        """
        self.tokens = Tokenizer(filename, options, keyword_manager).tokenize()
        self.filename = filename
        self.options = options
        self.keyword_manager = keyword_manager
        self.numbers = []


class ParserNumber(BaseParser):
    def is_match_number_patterns(self, token, end_token):
        pass


class ParserUtils(BaseParser):
    def is_anime_season_keyword(self, tokens: Tuple[Token, Token, Token]):
        prev_token, token, end_token = tokens
        target_token: Union[Token, None] = None
        part_token: Union[Token, None] = None
        if prev_token:
            number = get_number_from_ordinal(prev_token.content)
            if number:
                target_token = prev_token
                part_token = self.tokens.find_next(end_token, type_not_in=[TokenType.DELIMITER])
        else:
            next_token = self.tokens.find_next(end_token, type_not_in=[TokenType.DELIMITER])
            if next_token and next_token.content.isdigit():
                target_token = next_token
                part_token = self.tokens.find_next(next_token, type_not_in=[TokenType.DELIMITER])

        if target_token:
            # TODO: Should it in parser_options?
            if part_token and part_token.content.lower() == "part":

                part_number_token = self.tokens.find_next(part_token, type_not_in=[TokenType.DELIMITER])
                if part_number_token and part_number_token.content.isdigit():
                    if self.options.season_part_as_unique:
                        return
                    # Otherwise, ignore the part
                    part_token.type = TokenType.INVALID
                    part_number_token.type = TokenType.INVALID

            set_token(token, TokenType.IDENTIFIER, ElementCategory.ANIME_SEASON_PREFIX)
            for tok in self.tokens.loop_forward(token, end_token):
                tok.category = ElementCategory.ANIME_SEASON_PREFIX
                tok.remove_possibility()

            number = get_number_from_ordinal(target_token.content)
            if number:
                target_token.content = str(number)

            set_token(target_token, TokenType.IDENTIFIER, ElementCategory.ANIME_SEASON)

            if target_token in self.numbers:
                self.numbers.remove(target_token)

        return

    def is_episode_number(self, tokens: Tuple[Token, Token, Token]):
        prev_token, token, end_token = tokens
        next_token = self.tokens.find_next(token, type_not_in=[TokenType.DELIMITER])
        if next_token in constant.RANGE_SEPARATOR:
            pass


class ParserProcessor(ParserUtils):
    """
    All method to process tokens in each stage
    """

    def pre_process_numerical_token(self, token: Token, prev: Token, word: str):
        # Process CRC32
        if len(word) == 8:
            try:
                int(word, 16)
                set_token(token, TokenType.IDENTIFIER, ElementCategory.FILE_CHECKSUM)
                return
            except ValueError:
                pass

        # TODO: Should it in parser_options?
        if prev and prev.content.lower() == "part" and len(word) == 1:
            return

        # Process FILE_INDEX, ANIME_YEAR, or VIDEO_RESOLUTION
        if token.content.isdigit() and int(token.content) >= self.options.min_anime_year:
            token.add_possibility(ElementCategory.ANIME_YEAR)

        if not prev:
            token.add_possibility(ElementCategory.FILE_INDEX)
        elif self.options.video_resolution_pattern.match(word):
            set_token(token, TokenType.IDENTIFIER, ElementCategory.VIDEO_RESOLUTION)
            return
        elif prev in self.tokens.lookup_possibilities[ElementCategory.AUDIO_TERM]:
            token.add_possibility(ElementCategory.AUDIO_TERM)
        self.numbers.append(token)

    def pre_process_keyword_token(self, keyword: Keyword, tokens: Tuple[Token, Token, Token]):
        prev_token, token, end_token = tokens
        for next_token in self.tokens.loop_forward(token, end_token):
            next_token.add_possibility(keyword.category)

        if not ElementCategory.is_searchable(keyword.category):
            return

        if not keyword.options.searchable:
            if keyword.category == ElementCategory.ANIME_TYPE:
                next_token = self.tokens.find_next(end_token, type_not_in=[TokenType.DELIMITER])
                # Valid if:
                # it at the end of the filename
                # After a context delimiter
                if not next_token or is_context_delimiter(prev_token):
                    token.category = ElementCategory.ANIME_TYPE
                    token.type = TokenType.IDENTIFIER
            return

        if not keyword.options.identifiable and token.nest_level == 0:
            return

        if not keyword.options.valid:
            if not prev_token or not is_context_delimiter(prev_token):
                return

        if keyword.category == ElementCategory.ANIME_SEASON_PREFIX:
            self.is_anime_season_keyword(tokens)
            return
        if keyword.category == ElementCategory.EPISODE_PREFIX and keyword.options.valid:
            self.is_episode_number(tokens)
            return

        if keyword.category == ElementCategory.RELEASE_INFORMATION:
            if prev_token and prev_token.content.lower() in keyword.invalid_prefix:
                return
            token.category = ElementCategory.RELEASE_INFORMATION
            token.type = TokenType.IDENTIFIER
            return


class Parser(ParserProcessor):

    def search_for_keywords(self):
        """
        This function will search for keywords about:
        - Anime season prefix
        - Episode number prefix
        - Volume number prefix
        - Release Version
        - File CRC32
        - Video resolution
        - Any identifiable keywords, keywords.options["default"]
        """
        prev_token: Union[Token, None] = None
        have_release_group = False
        for token in self.tokens:
            if token.type == TokenType.DELIMITER:
                continue

            # TODO: What should get stripped?
            word = token.content.strip(f' {self.options.context_delimiter}')

            if not word:
                continue

            # skip if it is a number and not a CRC number
            if word.isdigit():
                self.pre_process_numerical_token(token, prev_token, word)
                prev_token = token
                continue

            keyword, end_token = self.keyword_manager.find_all(self.tokens, token)
            if keyword:
                self.pre_process_keyword_token(keyword, (prev_token, token, end_token))
            elif token.nest_level > 0:
                # it in bracket
                if (have_release_group is False or
                        ElementCategory.RELEASE_GROUP in prev_token.possibilities):
                    token.add_possibility(ElementCategory.RELEASE_GROUP)
                    have_release_group = True

            prev_token = token

    def parser(self):
        if not self.tokens:
            return None

        self.search_for_keywords()
