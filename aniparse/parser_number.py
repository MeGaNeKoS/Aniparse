import re
from typing import Tuple

from aniparse import KeywordManager, helper, ElementCategory, constant, parser_helper, Keyword
from aniparse.token import Tokens, TokenType, Token

ANIME_YEAR_MIN = 1900
ANIME_YEAR_MAX = 2100


class Base:
    def __init__(self, tokens: Tokens, options: dict, keyword_manager: KeywordManager):
        """
        Initialize a Base object.

        Args:
            tokens (Tokens): The Tokens object containing the tokens to be parsed.
            options (dict): A dictionary of options for parsing.
            keyword_manager (KeywordManager): A KeywordManager object containing the pre-identifier keywords to be used during parsing.
        """
        self.tokens = tokens
        self.options = options
        self.keyword_manager = keyword_manager
        self.candidates = {}

    def insert_tokens(self, base_token: Token,
                      tokens_list: Tuple, categories: list[ElementCategory]) -> Token:
        loop_skip_next = base_token.next
        for content, category in zip(reversed(tokens_list), reversed(categories), strict=True):
            if not content:
                continue
            token = Token(content, _type=TokenType.IDENTIFIER, category=category, enclosed=base_token.enclosed)
            self.tokens.insert_after(base_token, token)

        # merge and remove the first new token
        replaced_token = base_token.next
        base_token.content = replaced_token.content
        base_token.category = replaced_token.category
        self.tokens.remove(replaced_token)

        real_next_token = base_token.next

        base_token.next = loop_skip_next

        return real_next_token


class EpisodePattern(Base):
    _re_season_episode = re.compile(r"^(?:(s)?(\d+)"  # Season prefix or number
                                    r"(?:([" + constant.DASHES_PATTERN +
                                    r" ~&+])"  # separator
                                    r"(s)?(\d+))?)"  # 2nd season prefix or number
                                    # Season "1", "s01", "s01-02", "s01~02"
                                    r"(?:(x)|([" + constant.DASHES_PATTERN +
                                    r" ._\-x:])?(e))"  # Season-Episode separator
                                    r"(\d+(?:\.\d+)?)(?:(v)(\d+))?"  # Episode "01", "01v2"
                                    r"(?:([" + constant.DASHES_PATTERN +
                                    r"~&+])(e)?"  # Episode range separator
                                    r"(\d+(?:\.\d+)?)(?:(v)(\d+))?)?$",  # Episode "01", "01v2"
                                    flags=re.IGNORECASE)

    def is_match_season_and_episode_pattern(self, token: Token) -> Token:
        """
        Check if the given word matches a valid season and episode pattern.
        A valid pattern consists of:
        - a season number or prefix followed by a season number, with an optional range separator and season prefix/number
        - a season episode separator, e.g. "x" or "[range_separator]e"
        - an episode number with an optional release version
        - an optional range separator, episode prefix, and episode number with an optional release version
        Examples of valid patterns:
        e.g "2x01", "2x01v2"
        e.g "s01e03", "s01e03v2"
        e.g "s01-02xe001-150", "s01-02xe001-150v2", "s01-02xe001v3-150v2"
        e.g "s01-s02xe001-150", "s01-s02xe001-150v2", "s01-s02xe001v3-150v2"
        e.g "s01e03-s02e04", "s01e03-s02e04v2", "s01e03v4-s02e04v2"
        e.g "s01e03-04", "s01e03-04v2", "s01e03v4-04v2"
        assuming, previous was season: "01-02e03", "01-02e03v2", "01v3-s02e03v2"

        pattern:
        (<season_prefix><season_number>[<range_separator>[season_prefix]<season_number>])
        (<range_separator>|[range_separator]<episode_prefix>)
        <episode_number>[v<release_version>]
        [<range_separator>[episode_prefix]<episode_number>[v<release_version>]]

        Args:
        token: The current token being parsed.
        word: The word to check for a season and episode pattern.

        Returns:
            Tuple of True and real next token
            if the given word matches a valid season and episode pattern.
            Otherwise, Tuple of False and current token.
        """

        match = self._re_season_episode.match(token.content)

        if match:
            # check for lower bound < upper bound
            season_lower_bound = match.group(2)
            season_upper_bound = match.group(5)
            episode_lower_bound = match.group(9)
            episode_upper_bound = match.group(14)

            if season_upper_bound and int(season_lower_bound) > int(season_upper_bound):
                return token
            if episode_upper_bound and int(episode_lower_bound) > int(episode_upper_bound):
                return token

            try:
                if int(season_lower_bound) == 0 and token.enclosed:
                    # Avoid fansubbers [0x539] as season pattern
                    return token
            except ValueError:
                pass

            categories = [
                ElementCategory.ANIME_SEASON_PREFIX,
                ElementCategory.ANIME_SEASON,
                ElementCategory.RANGE_SEPARATOR,
                ElementCategory.ANIME_SEASON_PREFIX,
                ElementCategory.ANIME_SEASON,
                ElementCategory.RANGE_SEPARATOR,
                ElementCategory.RANGE_SEPARATOR,
                ElementCategory.EPISODE_PREFIX,
                ElementCategory.EPISODE_NUMBER,
                ElementCategory.RELEASE_VERSION_PREFIX,
                ElementCategory.RELEASE_VERSION,
                ElementCategory.RANGE_SEPARATOR,
                ElementCategory.EPISODE_PREFIX,
                ElementCategory.EPISODE_NUMBER,
                ElementCategory.RELEASE_VERSION_PREFIX,
                ElementCategory.RELEASE_VERSION,
            ]
            return self.insert_tokens(token, match.groups(), categories=categories)

        return token


class VolumePattern(Base):
    pass


class Pattern(EpisodePattern, VolumePattern):
    _re_match_multi_number = re.compile(r"(\d+(?:\.\d+)?)(?:(v)(\d+))?"  # Episode number, release version
                                        r"([" + constant.DASHES_PATTERN + r" ~&+])"  # Range separator
                                        r"(\d+(?:\.\d+)?)(?:(v)(\d+))?$",
                                        # Episode number, release version
                                        flags=re.IGNORECASE)
    _re_match_single_number = re.compile((r'^(\d+(?:\.\d+)?)'  # Episode number
                                          r'(?:(v)(\d+))?$'),  # Release version
                                         flags=re.IGNORECASE)

    def is_match_multi_numbers_pattern(self, token: Token, category: ElementCategory) -> Token:
        """
        Check if the word is a multi numbers pattern.
        e.g. "01-02", "01-02v2", "01v2-02v2", "01v2-02", "04.5-05.5", "04.5-05.5v2", "04.5v2-05.5v2", "04.5v2-05.5"
        pattern = <episode_number>[v<release_version>]<range_separator><episode_number>[v<release_version>]
        """
        match = self._re_match_multi_number.match(token.content)
        if match:
            if match.group(1) > match.group(5):
                return token
            categories = [
                (ElementCategory.EPISODE_NUMBER if category == ElementCategory.EPISODE_NUMBER
                 else ElementCategory.VOLUME_NUMBER),
                ElementCategory.RELEASE_VERSION_PREFIX,
                ElementCategory.RELEASE_VERSION,
                ElementCategory.RANGE_SEPARATOR,
                (ElementCategory.EPISODE_NUMBER if category == ElementCategory.EPISODE_NUMBER
                 else ElementCategory.VOLUME_NUMBER),
                ElementCategory.RELEASE_VERSION_PREFIX,
                ElementCategory.RELEASE_VERSION,
            ]

            return self.insert_tokens(token, match.groups(), categories=categories)
        return token

    def is_match_number_patterns(self, token: Token, category: ElementCategory, prefixed, prefix_category) -> Token:
        match_single_number = self.is_match_single_number_pattern(token, category, prefixed)
        if match_single_number != token:
            return match_single_number

        match_multi_number = self.is_match_multi_numbers_pattern(token, category)
        if match_multi_number != token:
            return match_multi_number

        check_for_season = True
        if prefixed:
            if prefix_category in [ElementCategory.EPISODE_PREFIX, ElementCategory.VOLUME_PREFIX]:
                check_for_season = False
        if check_for_season:
            match_season_episode = self.is_match_season_and_episode_pattern(token)
            if match_season_episode != token:
                return match_season_episode

        match_season_episode = self.is_match_partial_number_patterns(token, category, prefixed)
        if match_season_episode != token:
            return match_season_episode

        return token

    def is_match_partial_number_patterns(self, token: Token, category: ElementCategory, prefixed) -> Token:
        """
        Check if the word have a valid partial numbered pattern.
        e.g. "4a", "111C
        """
        non_number_begin = parser_helper.find_first_alpha(token.content)
        suffix = token.content[non_number_begin:]

        if non_number_begin and len(suffix) == 1 and suffix.isalpha():
            if not prefixed:
                if ElementCategory.EPISODE_NUMBER not in self.candidates:
                    self.candidates[ElementCategory.EPISODE_NUMBER] = []
                self.candidates[ElementCategory.EPISODE_NUMBER].append((token,
                                                                        (token.content[:non_number_begin], suffix),
                                                                        (ElementCategory.EPISODE_NUMBER,
                                                                         ElementCategory.EPISODE_PART)))
                return token

            episode_part = token.content[non_number_begin:]
            if category == ElementCategory.BONUS_NUMBER:
                episode_part_category = ElementCategory.BONUS_PART
            else:
                episode_part_category = ElementCategory.EPISODE_PART

            episode_part_token = Token(episode_part, _type=TokenType.IDENTIFIER,
                                       category=episode_part_category, enclosed=token.enclosed)
            token.content = token.content[:non_number_begin]
            token.category = category
            self.tokens.insert_after(token, episode_part_token)
            token.next = episode_part_token.next
            return episode_part_token
        return token

    def is_match_single_number_pattern(self, token: Token, category: ElementCategory, prefixed) -> Token:
        """
        Check if the word have a valid single numbered pattern.
        e.g. "01", "01v2", "07.5", "07.5v2"
        pattern = <episode_number>[v<release_version>]
        """
        match = self._re_match_single_number.match(token.content)
        if match:
            categories = [
                category,
                ElementCategory.RELEASE_VERSION_PREFIX,
                ElementCategory.RELEASE_VERSION,
            ]
            if not prefixed:
                # Required for all to be valid
                if category not in self.candidates:
                    self.candidates[category] = []
                self.candidates[category].append((token, match.groups(), categories))
                # and str(helper.get_number(match.group(1))) == match.group(1)
                if not all(match.groups()):
                    return token
                self.candidates.get(category, []).clear()
            return self.insert_tokens(token, match.groups(), categories=categories)
        return token


class ParserNumber(Pattern):
    def is_have_additional_prefix(self, token: Token, prefix, number, keyword, category):
        additional_prefix = parser_helper.find_first_alpha(number)
        left_over = None
        if additional_prefix:
            left_over = number[additional_prefix:]
            new_number_begin = parser_helper.find_first_number(left_over)
            key = left_over[:new_number_begin]
            lo_keyword = self.keyword_manager.find(
                self.keyword_manager.normalize(key)
            )
            if (lo_keyword
                    and lo_keyword.category in [ElementCategory.ANIME_TYPE,
                                                ElementCategory.BONUS_TYPE]):
                number = number[:additional_prefix]
            else:
                if key.lower() == "s":
                    new_token = Token(prefix, TokenType.IDENTIFIER,
                                      ElementCategory.ANIME_SEASON_PREFIX, enclosed=token.enclosed)
                    self.tokens.insert_before(token, new_token)
                    new_token = Token(number[:additional_prefix], TokenType.IDENTIFIER,
                                      ElementCategory.ANIME_SEASON, enclosed=token.enclosed)
                    self.tokens.insert_before(token, new_token)

                    number = left_over[new_number_begin:]
                    prefix = key
                    keyword = Keyword(ElementCategory.ANIME_TYPE, keyword.options)
                    category = ElementCategory.EPISODE_NUMBER

                left_over = None

        return left_over, number, prefix, keyword, category

    def is_number_comes_after_prefix(self, token: Token) -> Token:
        number_begin = parser_helper.find_first_number(token.content)

        if not number_begin:
            return token

        prefix = token.content[:number_begin]

        keyword = self.keyword_manager.find(
            self.keyword_manager.normalize(prefix)
        )

        if keyword:
            if keyword.category not in [ElementCategory.EPISODE_PREFIX, ElementCategory.VOLUME_PREFIX,
                                        ElementCategory.ANIME_SEASON_PREFIX, ElementCategory.ANIME_TYPE,
                                        ElementCategory.BONUS_TYPE]:
                return token

            number = token.content[number_begin:]
            if keyword.category == ElementCategory.ANIME_SEASON_PREFIX:
                category = ElementCategory.ANIME_SEASON
                left_over, number, prefix, keyword, category = self.is_have_additional_prefix(
                    token,
                    prefix,
                    number,
                    keyword,
                    category
                )
            elif keyword.category == ElementCategory.ANIME_TYPE:
                category = ElementCategory.EPISODE_NUMBER
            elif keyword.category == ElementCategory.BONUS_TYPE:
                category = ElementCategory.BONUS_NUMBER
            elif keyword.category == ElementCategory.EPISODE_PREFIX:
                category = ElementCategory.EPISODE_NUMBER
            elif keyword.category == ElementCategory.VOLUME_PREFIX:
                category = ElementCategory.VOLUME_NUMBER
            else:
                return token

            candidate = Token(number, category=category, enclosed=token.enclosed)
            self.tokens.insert_after(token, candidate)
            token.content = prefix

            match_number = self.is_match_number_patterns(candidate, category, True, keyword.category)
            if match_number != candidate:
                token.next = candidate.next
                token.category = keyword.category
                candidate.next = match_number
                self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                try:
                    if left_over:
                        lo_token = Token(left_over)
                        self.tokens.insert_after(candidate, lo_token)
                        match_number_after_pref = self.is_number_comes_after_prefix(lo_token)
                        if match_number_after_pref != lo_token:
                            lo_token.next = match_number_after_pref
                except NameError:
                    pass
                return candidate

            self.tokens.remove(candidate)
            token.content += number

        elif not prefix:  # if keyword
            return token
        else:
            number = token.content[number_begin:]
            if prefix.lower() == "v" and helper.is_number(number):
                original_next = token.next
                candidate = Token(number, category=ElementCategory.RELEASE_VERSION, enclosed=token.enclosed)
                self.tokens.insert_after(token, candidate)
                token.content = prefix
                token.category = ElementCategory.RELEASE_VERSION_PREFIX
                token.next = original_next
                return candidate

            if prefix[-1].lower() == "v" and helper.is_number(number):
                keyword = self.keyword_manager.find(
                    self.keyword_manager.normalize(prefix[:-1])
                )
                if keyword and keyword.category in [ElementCategory.EPISODE_PREFIX, ElementCategory.VOLUME_PREFIX,
                                                    ElementCategory.ANIME_SEASON_PREFIX, ElementCategory.ANIME_TYPE,
                                                    ElementCategory.BONUS_TYPE]:
                    initial_next = token.next
                    release_version = Token(number, category=ElementCategory.RELEASE_VERSION, enclosed=token.enclosed)
                    self.tokens.insert_after(token, release_version)
                    release_prefix = Token(token.content[number_begin - 1],
                                           category=ElementCategory.RELEASE_VERSION_PREFIX, enclosed=token.enclosed)
                    self.tokens.insert_after(token, release_prefix)
                    token.content = prefix[:-1]
                    token.category = keyword.category
                    token.next = initial_next
                    return release_prefix
                else:
                    if not token.prev or token.prev.type == TokenType.DELIMITER:
                        if not token.next or token.next.type == TokenType.DELIMITER:
                            initial_next = token.next
                            release_version = Token(number, category=ElementCategory.RELEASE_VERSION,
                                                    enclosed=token.enclosed)
                            self.tokens.insert_after(token, release_version)
                            token.content = prefix
                            token.category = ElementCategory.RELEASE_VERSION_PREFIX
                            token.next = initial_next
                            return release_version
        return token

    def valid_number_pattern(self, token: Token) -> Token:
        # if token is in the beginning of the string and the next token is dash.
        if token.prev is None:
            next_token = token.find_next(type_not_in=TokenType.DELIMITER)

            if helper.is_dash_character(next_token.content):
                self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                token.type = TokenType.IDENTIFIER
                token.category = ElementCategory.EPISODE_NUMBER
                next_token.type = TokenType.IDENTIFIER
                token.category = ElementCategory.EPISODE_NUMBER
                token.type = TokenType.IDENTIFIER
                real_token = token.next
                token.next = next_token
                return real_token
            return token

        prev_token = token.find_prev(type_not_in=TokenType.DELIMITER)
        prefixed = False
        if prev_token:
            if helper.is_dash_character(prev_token.content):
                prefixed = True
                match_pattern = self.is_match_number_patterns(token, ElementCategory.EPISODE_NUMBER,
                                                              prefixed,
                                                              ElementCategory.UNKNOWN)
                if match_pattern != token:
                    return match_pattern

            if str(prev_token.content).lower() in ['part']:
                return token

            if prev_token.category in [ElementCategory.EPISODE_PREFIX,
                                       ElementCategory.ANIME_SEASON,
                                       ElementCategory.ANIME_TYPE,
                                       ElementCategory.BONUS_TYPE]:
                if helper.is_number(token.content):
                    self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                    if prev_token.category == ElementCategory.BONUS_TYPE:
                        token.category = ElementCategory.BONUS_NUMBER
                    else:
                        token.category = ElementCategory.EPISODE_NUMBER
                    return token
                else:
                    return self.is_number_comes_after_prefix(token)

            if prev_token.category in [ElementCategory.ANIME_SEASON_PREFIX]:
                other_prev_token = prev_token.find_prev(type_not_in=TokenType.DELIMITER)
                if other_prev_token.category == ElementCategory.ANIME_SEASON:
                    self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                    token.category = ElementCategory.EPISODE_NUMBER
                    return token
                else:
                    token.category = ElementCategory.ANIME_SEASON
                    return token

        next_token = token.find_next(type_not_in=TokenType.DELIMITER)
        if next_token:
            separator = str(next_token.content)
            if separator.lower() in ("&", "of"):
                other_token = next_token.find_next(type_not_in=TokenType.DELIMITER)
                if other_token and helper.is_number(other_token.content):
                    if separator == "&":
                        next_token.type = TokenType.IDENTIFIER
                        token.type = TokenType.IDENTIFIER
                        self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                        other_token.category = ElementCategory.EPISODE_NUMBER
                    elif separator.lower() == "of":
                        if not helper.first_number_lower_than_second(token.content, other_token.content):
                            return token
                        next_token.type = TokenType.IDENTIFIER
                        token.type = TokenType.IDENTIFIER
                        other_token.category = ElementCategory.EPISODE_TOTAL
                    token.type = TokenType.IDENTIFIER
                    self.candidates.get(ElementCategory.EPISODE_NUMBER, []).clear()
                    token.category = ElementCategory.EPISODE_NUMBER
                    return other_token

        number_come_after_prefix = self.is_number_comes_after_prefix(token)
        if number_come_after_prefix != token:
            return number_come_after_prefix

        match_number = self.is_match_number_patterns(token, ElementCategory.EPISODE_NUMBER, prefixed, ElementCategory.UNKNOWN)
        if match_number != token:
            return match_number

        return token
