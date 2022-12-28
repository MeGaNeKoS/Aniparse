import logging

from aniparse import parser_helper, KeywordManager, constant, helper
from aniparse.element import ElementCategory
from aniparse.parser_number import ParserNumber
from aniparse.token import TokenType
from aniparse.tokenizer import Tokenizer

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, filename: str, options: dict, keyword_manager: KeywordManager):
        """
        Initialize a Parser object.

        Args:
            filename (str): The string representing the filename to be parsed.
            options (dict): A dictionary of options for parsing.
            keyword_manager (KeywordManager): A KeywordManager object containing the pre-identifier keywords to be used during parsing.
        """
        self.tokens = Tokenizer(filename, options['allowed_delimiters'], keyword_manager).tokenize()
        self.options = options
        self.keyword_manager = keyword_manager

    def parse(self) -> None:
        if not self.tokens:
            return None
        parser_number = ParserNumber(self.tokens, self.options, self.keyword_manager)
        current_category = ElementCategory.UNKNOWN
        loop_skipper = tuple()
        verified_later = []
        have_release_group = False

        for token in self.tokens.loop_forward():
            if token.type != TokenType.UNKNOWN:
                # we have already parsed this token
                continue

            if loop_skipper:
                loop_skipper[0].next = loop_skipper[1]
                loop_skipper = tuple()

            word = token.content
            word = word.strip(f' {constant.DASHES}')

            if token.content in constant.DASHES:
                if current_category == ElementCategory.ANIME_TITLE:
                    current_category = ElementCategory.EPISODE_NUMBER
                    token.type = TokenType.IDENTIFIER
                continue

            if not word:
                continue

            keyword = self.keyword_manager.find(self.keyword_manager.normalize(word))

            if keyword:
                category = keyword.category

                if category == ElementCategory.ANIME_SEASON_PREFIX:
                    # is_anime_season_keyword
                    prev_token = token.find_prev(type_not_in=TokenType.DELIMITER)
                    number = parser_helper.get_number_from_ordinal(prev_token.content)
                    if number:
                        prev_token.type = TokenType.IDENTIFIER
                        token.type = TokenType.IDENTIFIER
                        prev_token.content = number
                        prev_token.category = ElementCategory.ANIME_SEASON
                        token.category = ElementCategory.ANIME_SEASON_PREFIX
                        continue

                    next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                    if next_token and helper.is_number(next_token.content):
                        next_token.type = TokenType.IDENTIFIER
                        token.type = TokenType.IDENTIFIER
                        next_token.category = ElementCategory.ANIME_SEASON
                        token.category = ElementCategory.ANIME_SEASON_PREFIX
                        loop_skipper = token, token.next
                        token.next = next_token.next
                        continue

                elif category == ElementCategory.ANIME_TYPE:
                    prev_token = token.find_prev(type_not_in=TokenType.DELIMITER)
                    next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                    if next_token:
                        if helper.is_dash_character(prev_token.content) and helper.is_dash_character(
                                next_token.content):
                            token.type = TokenType.IDENTIFIER
                            token.category = ElementCategory.ANIME_TYPE
                            continue
                        if helper.is_dash_character(next_token.content):
                            token.type = TokenType.IDENTIFIER
                            token.category = ElementCategory.ANIME_TYPE
                            continue

                        if helper.is_number(next_token.content):
                            real_next_token = parser_number.is_match_number_patterns(next_token,
                                                                                     ElementCategory.EPISODE_NUMBER,
                                                                                     True,
                                                                                     ElementCategory.UNKNOWN)
                            if real_next_token != next_token:
                                parser_number.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                                token.type = TokenType.IDENTIFIER
                                token.category = category

                                if real_next_token != next_token.next:
                                    loop_skipper = (token, token.next)
                                    token.next = next_token.next
                                    next_token.next = real_next_token
                                else:
                                    loop_skipper = (token, token.next)
                                    token.next = real_next_token
                                continue
                            # next_token.type = TokenType.IDENTIFIER
                            # token.type = TokenType.IDENTIFIER
                            # token.category = ElementCategory.ANIME_TYPE
                            # loop_skipper = token, token.next
                            # token.next = next_token.next
                            continue
                        next_keyword = self.keyword_manager.find(self.keyword_manager.normalize(next_token.content))
                        if next_keyword:
                            token.type = TokenType.IDENTIFIER
                            token.category = category
                            next_token.type = TokenType.IDENTIFIER
                            next_token.category = next_keyword.category
                            loop_skipper = token, token.next
                            token.next = next_token.next
                            continue
                    else:
                        if prev_token and helper.is_dash_character(prev_token.content):
                            if not next_token or (
                                    next_token.type == TokenType.IDENTIFIER
                            ):
                                prev_token.type = TokenType.IDENTIFIER
                                token.type = TokenType.IDENTIFIER
                                token.category = ElementCategory.ANIME_TYPE
                        token.type = TokenType.IDENTIFIER
                        token.category = ElementCategory.ANIME_TYPE
                        continue

                elif category == ElementCategory.BONUS_TYPE:
                    prev_token = token.find_prev(type_not_in=TokenType.DELIMITER)
                    next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                    if token.content.lower() in ["opening", "ending"]:
                        if prev_token.content.lower() == "clean":
                            self.tokens.combine(prev_token, token, ElementCategory.BONUS_TYPE)

                    if next_token:
                        if helper.is_dash_character(prev_token.content) and helper.is_dash_character(
                                next_token.content):
                            token.type = TokenType.IDENTIFIER
                            token.category = ElementCategory.BONUS_TYPE
                            continue
                        real_next_token = parser_number.is_match_number_patterns(next_token,
                                                                                 ElementCategory.BONUS_NUMBER,
                                                                                 True,
                                                                                 ElementCategory.UNKNOWN)
                        if real_next_token != next_token:
                            parser_number.candidates.get(ElementCategory.BONUS_NUMBER, []).clear()
                            token.type = TokenType.IDENTIFIER
                            token.category = category

                            if real_next_token != next_token.next:
                                loop_skipper = (token, token.next)
                                token.next = next_token.next
                                next_token.next = real_next_token
                            else:
                                loop_skipper = (token, token.next)
                                token.next = real_next_token
                            continue
                        verified_later.append((token, category))
                        continue
                    else:
                        if prev_token and helper.is_dash_character(prev_token.content):
                            if not next_token or (
                                    next_token.type == TokenType.IDENTIFIER
                            ):
                                prev_token.type = TokenType.IDENTIFIER
                                token.type = TokenType.IDENTIFIER
                                token.category = ElementCategory.BONUS_TYPE
                            continue

                elif category in [ElementCategory.EPISODE_PREFIX,
                                  ElementCategory.VOLUME_PREFIX]:
                    next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                    if next_token and parser_helper.find_first_number(next_token.content) is not None:

                        if category == ElementCategory.VOLUME_PREFIX:
                            pattern_category = ElementCategory.VOLUME_NUMBER
                        else:
                            pattern_category = ElementCategory.EPISODE_NUMBER

                        real_next_token = parser_number.is_match_number_patterns(next_token,
                                                                                 pattern_category,
                                                                                 True,
                                                                                 category)
                        if real_next_token != next_token:
                            parser_number.candidates.get(pattern_category, []).clear()
                            token.type = TokenType.IDENTIFIER
                            token.category = category

                            if real_next_token != next_token.next:
                                loop_skipper = (token, token.next)
                                token.next = next_token.next
                                next_token.next = real_next_token
                            else:
                                loop_skipper = (token, token.next)
                                token.next = real_next_token
                            continue

                elif keyword.options.identifiable:
                    token.type = TokenType.IDENTIFIER
                    token.category = keyword.category
                    continue

                elif token.enclosed:
                    token.type = TokenType.IDENTIFIER
                    token.category = keyword.category
                    continue



            else:  # if keyword
                if parser_helper.find_first_number(word) is not None:
                    if parser_helper.is_resolution(word):
                        token.type = TokenType.IDENTIFIER
                        token.category = ElementCategory.VIDEO_RESOLUTION
                        continue
                    if token.enclosed:
                        if helper.get_number(word) in constant.RESOLUTIONS:
                            token.type = TokenType.IDENTIFIER
                            token.category = ElementCategory.VIDEO_RESOLUTION
                            continue

                        if len(word) == 4 and word.isdigit():
                            number = int(token.content)
                            if constant.ANIME_YEAR_MIN <= number <= constant.ANIME_YEAR_MAX:
                                token.type = TokenType.IDENTIFIER
                                token.category = ElementCategory.ANIME_YEAR
                                continue

                        prev_token = token.find_prev(type_not_in=TokenType.DELIMITER)
                        next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                        if prev_token.type == next_token.type == TokenType.BRACKET:

                            if not prev_token.find_prev(type_not_in=TokenType.DELIMITER):
                                continue
                            real_next_token = parser_number.is_number_comes_after_prefix(token)

                            if real_next_token != token:
                                if real_next_token != token.next:
                                    # the next token was modified to skip processed tokens
                                    loop_skipper = (token, real_next_token)
                                continue

                    if len(word) == 8 and helper.is_crc32(word):
                        token.type = TokenType.IDENTIFIER
                        token.category = ElementCategory.FILE_CHECKSUM
                        continue
                    # this can be an episode number. Try to parse it.
                    real_next_token = parser_number.valid_number_pattern(token)
                    if real_next_token != token:
                        if real_next_token != token.next:
                            # the next token was modified to skip processed tokens
                            loop_skipper = (token, real_next_token)
                        continue

                # if not have_release_group and token.enclosed:
                #     token.category = ElementCategory.RELEASE_GROUP
                #     next_token = token.next
                #     while next_token and next_token.type != TokenType.BRACKET:
                #         next_token.category = ElementCategory.RELEASE_GROUP
                #         next_token = next_token.next
                #     loop_skipper = (token, token.next)
                #     token.next = next_token
                #     have_release_group = True
                #     # avoid variable leak
                #     del next_token
                #     continue
                #
                # if current_category == ElementCategory.UNKNOWN:
                #     current_category = ElementCategory.ANIME_TITLE
                #
                # if current_category == ElementCategory.ANIME_TITLE:
                #     token.category = ElementCategory.ANIME_TITLE
                #
                # if current_category == ElementCategory.ANIME_SEASON:
                #     token.category = ElementCategory.ANIME_SEASON

        # Apply leftover tokens
        if loop_skipper:
            loop_skipper[0].next = loop_skipper[1]

        for token, category in reversed(verified_later):
            next_token = token.find_next(type_not_in=[TokenType.DELIMITER, TokenType.BRACKET])
            if next_token and next_token.type == TokenType.IDENTIFIER:
                token.type = TokenType.IDENTIFIER
                token.category = category
                continue

        for category, tokens in parser_number.candidates.items():
            for (token, groups, categories) in tokens:
                if category == ElementCategory.EPISODE_NUMBER:
                    next_token = token.find_next(type_not_in=TokenType.DELIMITER)
                    if not next_token or (next_token and helper.is_dash_character(next_token.content)):
                        if str(helper.get_number(token.content)) == token.content:
                            continue
                        parser_number.insert_tokens(token, groups, categories)
                    next_token = token.find_next(type_not_in=[TokenType.DELIMITER, TokenType.BRACKET])
                    if not next_token or (
                            next_token
                            and next_token.category in [ElementCategory.AUDIO_TERM,
                                                        ElementCategory.VIDEO_TERM,
                                                        ElementCategory.VIDEO_RESOLUTION,
                                                        ElementCategory.EPISODE_TITLE,
                                                        ElementCategory.RELEASE_INFORMATION,
                                                        ElementCategory.RELEASE_VERSION,
                                                        ElementCategory.RELEASE_VERSION_PREFIX,
                                                        ElementCategory.SOURCE,
                                                        ElementCategory.SUBTITLES,
                                                        ]):
                        parser_number.insert_tokens(token, groups, categories)

                    if str(helper.get_number(groups[0])) != groups[0]:
                        parser_number.insert_tokens(token, groups, categories)
