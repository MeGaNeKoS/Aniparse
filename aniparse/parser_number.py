import re
from typing import List

from aniparse import parser_helper
from aniparse.element import ElementCategory
from aniparse.keyword import Keyword
from aniparse.token import Token, TokenCategory, TokenFlags, Tokens

ANIME_YEAR_MIN = 1900
ANIME_YEAR_MAX = 2100


# noinspection DuplicatedCode
class EpisodePattern(Tokens):
    _re_japanese_counter = re.compile(r"^(第)?(\d+)"  # prefix
                                      r"(?:([" + parser_helper.ESCAPED_DASHES +
                                      r" ~&+]?)"  # prefix separator
                                      r"(\d+))?"  # number
                                      r"([話弾])$",  # prefix
                                      flags=re.IGNORECASE)
    _re_number_sign = re.compile(r"^(#)(\d+(?:\.\d+)?)"  # sign and number
                                 r"(?:([" + parser_helper.ESCAPED_DASHES +
                                 r" ~&+]?)"  # separator
                                 r"(\d+(?:\.\d+)?))?"  # 2nd number
                                 r"(?:(v)(\d+))?$",  # version
                                 flags=re.IGNORECASE)
    _re_season_episode = re.compile(r"^(?:(\d+)|(s)(\d+)"  # Season prefix or number
                                    r"(?:([" + parser_helper.ESCAPED_DASHES +
                                    r" ~&+])"  # separator
                                    r"(s)?(\d+))?)"  # 2nd season prefix or number
                                    # Season "1", "s01", "s01-02", "s01~02"
                                    r"(?:(x)|([" + parser_helper.ESCAPED_DASHES +
                                    r" ._\-x:])?(e))"  # Season-Episode separator
                                    r"(\d+(?:\.\d+)?)(?:(v)(\d+))?"  # Episode "01", "01v2"
                                    r"(?:([" + parser_helper.ESCAPED_DASHES +
                                    r"~&+])(e)?"  # Episode range separator
                                    r"(\d+(?:\.\d+)?)(?:(v)(\d+))?)?$",  # Episode "01", "01v2"
                                    flags=re.IGNORECASE)

    def is_match_japanese_counter_pattern(self, token: Token, word: str) -> bool:
        """
        Checking for japanese style counter pattern

        e.g. "01話", "第01話", "第02-03話"
        pattern
        <japanese counter><episode number>[<range_separator><episode number>]
        """
        match = self._re_japanese_counter.match(word)
        if match:
            if match.group(5):
                self.insert_tokens(token, match.group(5), TokenCategory.IDENTIFIER, ElementCategory.UNKNOWN)
            if match.group(4):
                self.insert_tokens(token, match.group(4), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            if match.group(3):
                self.insert_tokens(token, match.group(3), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(2):
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                token.content = match.group(2)
            if match.group(1):
                new_token = Token(match.group(1), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX,
                                  token.enclosed)
                self.insert_before(token, new_token)
            return True
        return False

    def is_match_number_sign_pattern(self, token: Token, word: str) -> bool:
        """
        Checking for number sign pattern
        e.g. "#01", "#02-03v2"
        pattern
        <number sign><episode number>[<range_separator><episode number>][<version>]
        """
        match = self._re_number_sign.match(word)
        if match:
            if match.group(6):
                self.insert_tokens(token, match.group(6), TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION)
            if match.group(5):
                self.insert_tokens(token, match.group(5), TokenCategory.INVALID, ElementCategory.UNKNOWN)
            if match.group(4):
                self.insert_tokens(token, match.group(4), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            if match.group(3):
                self.insert_tokens(token, match.group(3), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(2):
                self.insert_tokens(token, match.group(2), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX)

            token.content = match.group(1)
            return True
        return False

    def is_match_season_and_episode_pattern(self, token: Token, word: str) -> bool:
        """
        Checking for season and episode pattern
        e.g "2x01", "2x01v2"
        e.g "s01e03", "s01e03v2"
        e.g "s01-02xe001-150", "s01-02xe001-150v2", "s01-02xe001v3-150v2"
        e.g "s01-s02xe001-150", "s01-s02xe001-150v2", "s01-s02xe001v3-150v2"
        e.g "s01e03-s02e04", "s01e03-s02e04v2", "s01e03v4-s02e04v2"
        e.g "s01e03-04", "s01e03-04v2", "s01e03v4-04v2"
        assuming, previous was season: "01-02e03", "01-02e03v2", "01v3-s02e03v2"
        pattern:
        (<season_number>|<season_prefix><season_number>[<range_separator>[season_prefix]<season_number>])
        (<range_separator>|[range_separator]<episode_prefix>)
        <episode_number>[v<release_version>][<range_separator>[episode_prefix]<episode_number>[v<release_version>]]
        """

        match = self._re_season_episode.match(word)

        if match:
            # check for lower bound < upper bound
            season_lower_bound = match.group(1) or match.group(3)
            season_upper_bound = match.group(6)
            episode_lower_bound = match.group(10)
            episode_upper_bound = match.group(15)

            if season_upper_bound and int(season_lower_bound) > int(season_upper_bound):
                return False
            if episode_upper_bound and int(episode_lower_bound) > int(episode_upper_bound):
                return False
            try:
                if int(season_lower_bound) == 0 and token.enclosed:
                    # Avoid fansubbers [0x539] as season pattern
                    return False
            except ValueError:
                pass
            # in reverse order to keep the order of tokens
            if match.group(17):
                self.insert_tokens(token, match.group(17), TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION)
            if match.group(16):
                self.insert_tokens(token, match.group(16), TokenCategory.INVALID, ElementCategory.UNKNOWN)
            if match.group(15):
                self.insert_tokens(token, episode_upper_bound, TokenCategory.IDENTIFIER,
                                   ElementCategory.EPISODE_NUMBER)
            if match.group(14):
                self.insert_tokens(token, match.group(14), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX)
            if match.group(13):
                self.insert_tokens(token, match.group(13), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(12):
                self.insert_tokens(token, match.group(12), TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION)
            if match.group(11):
                self.insert_tokens(token, match.group(11), TokenCategory.INVALID, ElementCategory.UNKNOWN)
            if match.group(10):
                self.insert_tokens(token, match.group(10), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            if match.group(9):
                self.insert_tokens(token, match.group(9), TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX)
            if match.group(8):
                self.insert_tokens(token, match.group(8), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(7):
                self.insert_tokens(token, match.group(7), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(6):
                self.insert_tokens(token, match.group(6), TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
            if match.group(5):
                self.insert_tokens(token, match.group(5), TokenCategory.IDENTIFIER,
                                   ElementCategory.ANIME_SEASON_PREFIX)
            if match.group(4):
                self.insert_tokens(token, match.group(4), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
            if match.group(2):
                if match.group(3):
                    self.insert_tokens(token, match.group(3), TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
                token.content = match.group(2)
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON_PREFIX)
            elif match.group(1):
                token.content = match.group(1)
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
            return True
        return False


class VolumePattern(Tokens):
    pass


class Pattern(EpisodePattern, VolumePattern):
    """
    Main pattern that apply for Episode, Volume, and Season.
    """
    _re_match_multi_number = re.compile(r"(\d+(?:\.\d+)?)(?:(v)(\d+))?"  # Episode number, release version
                                        r"([" + parser_helper.ESCAPED_DASHES +
                                        r" ~&+])"  # Range separator
                                        r"(\d+(?:\.\d+)?)(?:(v)(\d+))?$",  # Episode number, release version
                                        flags=re.IGNORECASE)
    _re_match_single_number = re.compile((r'^(\d+(?:\.\d+)?)'  # Episode number
                                          r'(?:(v)(\d+))?$'),  # Release version
                                         flags=re.IGNORECASE)

    def is_match_multi_numbers_pattern(self, token: Token, word: str, category: ElementCategory) -> bool:
        """
        Check if the word is a multi numbers pattern.
        e.g. "01-02", "01-02v2", "01v2-02v2", "01v2-02", "04.5-05.5", "04.5-05.5v2", "04.5v2-05.5v2", "04.5v2-05.5"
        pattern = <episode_number>[v<release_version>]<range_separator><episode_number>[v<release_version>]
        """
        match = self._re_match_multi_number.match(word)
        if match:
            lower_bound = match.group(1)
            upper_bound = match.group(5)
            # Avoid matching expressions such as "009-1" or "5-2"
            if int(lower_bound) < int(upper_bound):

                # In reverse order to keep the order of tokens
                if match.group(7):
                    self.insert_tokens(token, match.group(7), TokenCategory.IDENTIFIER,
                                       ElementCategory.RELEASE_VERSION)
                if match.group(6):
                    self.insert_tokens(token, match.group(6), TokenCategory.INVALID, ElementCategory.UNKNOWN)
                # match group 5 is the upper bound
                self.insert_tokens(token, upper_bound, TokenCategory.IDENTIFIER, category)
                # match group 4 is the range separator
                self.insert_tokens(token, match.group(4), TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
                if match.group(3):
                    self.insert_tokens(token, match.group(3), TokenCategory.IDENTIFIER,
                                       ElementCategory.RELEASE_VERSION)
                if match.group(2):
                    self.insert_tokens(token, match.group(2), TokenCategory.INVALID, ElementCategory.UNKNOWN)

                # match.group(1) is the lower bound
                self.set_token_element(token, TokenCategory.IDENTIFIER, category)
                token.content = lower_bound
                return True
        return False

    def is_match_number_patterns(self, token: Token, word: str, category: ElementCategory,
                                 prefix: bool = False) -> bool:
        """
        Check if the word have a valid numbered pattern.
        """
        if parser_helper.is_potential_number(word) and not prefix:
            # If the word only a number and the prefix is not set, then try to check the previous token
            previous_token = self.find_prev(token, TokenFlags.IDENTIFIER | TokenFlags.UNKNOWN)
            if previous_token.content.lower() in ["part"]:
                return False
            if previous_token.t_category in [TokenCategory.DELIMITER, TokenCategory.BRACKET]:
                self.set_token_element(previous_token, TokenCategory.INVALID, ElementCategory.UNKNOWN)
                self.set_token_element(token, TokenCategory.IDENTIFIER, category)
                return True
            if parser_helper.is_dash_character(previous_token.content):
                self.set_token_element(token, TokenCategory.IDENTIFIER, category)
                return True
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(previous_token.content))
            if keyword:
                if keyword.e_category in [ElementCategory.ANIME_SEASON, ElementCategory.ANIME_TYPE,
                                          ElementCategory.EPISODE_PREFIX]:
                    self.set_token_element(previous_token, TokenCategory.IDENTIFIER, keyword.e_category)
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                elif keyword.e_category in [ElementCategory.VOLUME_PREFIX]:
                    self.set_token_element(previous_token, TokenCategory.IDENTIFIER, keyword.e_category)
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.VOLUME_NUMBER)
                elif keyword.e_category in [ElementCategory.ANIME_SEASON_PREFIX]:
                    self.set_token_element(previous_token, TokenCategory.IDENTIFIER, keyword.e_category)
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
            # check if the next token is an unknown token and the content is "-"
            # if true, then it possibly an episode number
            next_token = self.find_next(token, TokenFlags.UNKNOWN | TokenFlags.IDENTIFIER)
            if next_token:
                if next_token.e_category in [
                    ElementCategory.AUDIO_TERM,
                    ElementCategory.VIDEO_TERM,
                    ElementCategory.VIDEO_RESOLUTION,
                    ElementCategory.EPISODE_TITLE,
                    ElementCategory.RELEASE_INFORMATION,
                    ElementCategory.RELEASE_VERSION,
                    ElementCategory.SOURCE,
                    ElementCategory.SUBTITLES,
                ]:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                    return True
                if previous_token == token and parser_helper.is_dash_character(next_token.content):
                    # found episode number-title separator
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                    return True
            return False

        word = word.strip(' ' + parser_helper.DASHES)
        numeric_front = word[0].isdigit()
        numeric_back = word[-1].isdigit()

        # e.g. "01v2"
        if numeric_front and numeric_back:
            if self.is_match_single_number_pattern(token, word, category):
                return True
            if self.is_match_multi_numbers_pattern(token, word, category):
                return True
        if self.is_match_season_and_episode_pattern(token, word):
            return True
        # only valid for episode numbers
        if category == ElementCategory.EPISODE_NUMBER:
            if numeric_back:
                if self.is_match_number_sign_pattern(token, word):
                    return True
            if self.is_match_japanese_counter_pattern(token, word):
                return True
        if prefix:
            if self.is_match_partial_number_patterns(token, word):
                return True
        return False

    def is_match_partial_number_patterns(self, token: Token, word: str) -> bool:
        """
        Check if the word have a valid partial numbered pattern.
        e.g. "4a", "111C
        """
        non_number_begin = parser_helper.find_non_number_in_string(word)
        suffix = word[non_number_begin:]

        if len(suffix) == 1 and suffix.isalpha():
            token.content = word[:non_number_begin]
            self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)

            number = word[non_number_begin:]
            self.insert_tokens(token, number, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PART)
            return True
        return False

    def is_match_single_number_pattern(self, token: Token, word: str, category: ElementCategory) -> bool:
        """
        Check if the word have a valid single numbered pattern.
        e.g. "01", "01v2", "07.5", "07.5v2"
        pattern = <episode_number>[v<release_version>]
        """
        match = self._re_match_single_number.match(word)
        if match:
            # in reverse order to keep the order of tokens
            if match.group(3):
                self.insert_tokens(token, match.group(3), TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION)
            if match.group(2):
                self.insert_tokens(token, match.group(2), TokenCategory.INVALID, ElementCategory.UNKNOWN)

            token.content = match.group(1)
            self.set_token_element(token, TokenCategory.IDENTIFIER, category)
            return True
        return False


class ParserNumber(Pattern):
    _re_search_buggy_dash = re.compile(r"(" + "|".join(parser_helper.DASHES) + r")",
                                       flags=re.IGNORECASE)

    def is_extent_keyword(self, token: Token, category: ElementCategory, prefix: bool) -> bool:
        next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
        if next_token and next_token.t_category == TokenCategory.UNKNOWN:
            if parser_helper.find_number_in_string(next_token.content) is not None:
                # Check for episode, and volume number
                if category in [ElementCategory.EPISODE_NUMBER, ElementCategory.VOLUME_NUMBER]:
                    if self.is_match_number_patterns(next_token, next_token.content, category, prefix):
                        return True
        return False

    def is_number_comes_after_prefix(self, token: Token) -> bool:
        number_begin = parser_helper.find_number_in_string(token.content)
        prefix = token.content[:number_begin]

        keyword = self.keyword_manager.find(
            self.keyword_manager.normalize(prefix)
        )
        if keyword:
            if keyword.e_category not in [ElementCategory.EPISODE_PREFIX, ElementCategory.VOLUME_PREFIX,
                                          ElementCategory.ANIME_SEASON_PREFIX, ElementCategory.ANIME_TYPE]:
                return False

            number = token.content[number_begin:]
            if keyword.e_category == ElementCategory.EPISODE_PREFIX:
                category = ElementCategory.EPISODE_NUMBER
            elif keyword.e_category == ElementCategory.VOLUME_PREFIX:
                category = ElementCategory.VOLUME_NUMBER
            elif keyword.e_category == ElementCategory.ANIME_SEASON_PREFIX:
                category = ElementCategory.ANIME_SEASON
                additional_prefix = parser_helper.find_non_number_in_string(number)
                if additional_prefix:
                    left_over = number[additional_prefix:]
                    new_number_begin = parser_helper.find_number_in_string(left_over)
                    key = left_over[:new_number_begin]
                    lo_keyword = self.keyword_manager.find(
                        self.keyword_manager.normalize(key)
                    )
                    if (lo_keyword
                            and lo_keyword.e_category == ElementCategory.ANIME_TYPE):
                        number = number[:additional_prefix]
                    else:
                        if key.upper() == "S":
                            new_token = Token(prefix,
                                              TokenCategory.IDENTIFIER,
                                              ElementCategory.ANIME_SEASON_PREFIX,
                                              token.enclosed)
                            self.insert_before(token, new_token)
                            new_token = Token(number[:additional_prefix],
                                              TokenCategory.IDENTIFIER,
                                              ElementCategory.ANIME_SEASON,
                                              token.enclosed)
                            self.insert_before(token, new_token)
                            keyword = Keyword(ElementCategory.ANIME_TYPE, keyword.options)
                            category = ElementCategory.EPISODE_NUMBER
                            prefix = key
                            number = left_over[new_number_begin:]
                        del left_over
            elif keyword.e_category == ElementCategory.ANIME_TYPE:
                category = ElementCategory.EPISODE_NUMBER
            else:
                return False

            if self.is_match_number_patterns(token, number, category, True):
                new_token = Token(prefix, TokenCategory.IDENTIFIER, keyword.e_category, token.enclosed)
                self.insert_before(token, new_token)
                try:
                    left_token = Token(left_over, TokenCategory.UNKNOWN, ElementCategory.UNKNOWN, token.enclosed)
                    self.insert_after(token, left_token)
                    self.is_number_comes_after_prefix(left_token)
                except NameError:
                    pass
                return True
        else:
            number = token.content[number_begin:]
            if prefix and prefix[-1].lower() == "v" and number.isdigit():
                keyword = self.keyword_manager.find(
                    self.keyword_manager.normalize(prefix[:-1])
                )
                if keyword and keyword.e_category in [ElementCategory.EPISODE_PREFIX, ElementCategory.VOLUME_PREFIX,
                                                      ElementCategory.ANIME_SEASON_PREFIX, ElementCategory.ANIME_TYPE]:
                    token.content = prefix[:-1]
                    self.set_token_element(token, TokenCategory.IDENTIFIER, keyword.e_category)
                    new_token = Token(prefix[-1], TokenCategory.INVALID, ElementCategory.UNKNOWN, token.enclosed)
                    self.insert_after(token, new_token)
                    new_token = Token(number, TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION, token.enclosed)
                    self.insert_after(token, new_token)
                    return True
        return False

    def is_number_comes_before_another_number(self, token: Token) -> bool:
        """
        Check if the number comes before another number.
        """
        separator_token = self.find_next(token, TokenFlags.NOT_DELIMITER)

        if separator_token:
            separator = separator_token.content
            if separator == "&" or str(separator).lower() == "of":
                other_token = self.find_next(separator_token, TokenFlags.NOT_DELIMITER)
                if other_token and other_token.content.isdigit():
                    if separator == "&":
                        self.set_token_element(other_token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)

                    elif str(separator).lower() == "of":
                        self.set_token_element(other_token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_TOTAL)

                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                    self.set_token_element(separator_token, TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)
                    return True
        return False

    def search_for_buggy_dash(self, tokens: List[Token]) -> None:
        """
        This is the last resort to fix the dash problem.
        e.g. "Gunbuster-ep1" -> "Gunbuster - ep1"

        :param tokens:
        :return:
        """
        for token in tokens:
            splitted = self._re_search_buggy_dash.split(token.content)
            placeholder = []
            new_token = Token("", token.t_category, token.e_category, token.enclosed)
            potential_tokens = []
            for text in splitted:
                if parser_helper.find_number_in_string(text) is not None:
                    if new_token.content:
                        # first and last dashes put on separate token
                        stripped_text = new_token.content.strip(parser_helper.DASHES)
                        dashes = new_token.content.split(stripped_text)
                        if dashes[0]:
                            placeholder.append(Token(dashes[0], TokenCategory.INVALID,
                                                     ElementCategory.UNKNOWN, token.enclosed))
                        new_token.content = stripped_text
                        placeholder.append(new_token)
                        if dashes[1]:
                            placeholder.append(Token(dashes[1], TokenCategory.INVALID,
                                                     ElementCategory.UNKNOWN, token.enclosed))

                        new_token = Token("", token.t_category, token.e_category, token.enclosed)
                    number_token = Token(text, token.t_category, token.e_category, token.enclosed)
                    placeholder.append(number_token)
                    potential_tokens.append(number_token)
                else:
                    new_token.content += text

            if new_token.content:
                stripped_text = new_token.content.strip(parser_helper.DASHES)
                dashes = new_token.content.split(stripped_text)
                if dashes[0]:
                    placeholder.append(Token(dashes[0], TokenCategory.INVALID,
                                             ElementCategory.UNKNOWN, token.enclosed))
                new_token.content = stripped_text
                placeholder.append(new_token)
                if dashes[1]:
                    placeholder.append(Token(dashes[1], TokenCategory.INVALID,
                                             ElementCategory.UNKNOWN, token.enclosed))

            if placeholder:
                placeholder.reverse()
                for i_token in placeholder:
                    self.insert_after(token, i_token)
                self.remove_token(token)

                is_found = False
                for potential_token in potential_tokens:
                    if self.is_number_comes_after_prefix(potential_token):
                        is_found = True
                    elif self.search_for_last_number([potential_token]):
                        is_found = True

                if not is_found:
                    self.insert_after(placeholder[-1], token)
                    for i_token in placeholder:
                        self.remove_token(i_token)
        return

    def search_for_equivalent_numbers(self, tokens: List[Token]) -> bool:
        """
        Search for equivalent numbers.
        """
        is_found = False
        for token in tokens:
            if self.is_token_isolated(token):
                continue

            previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
            if previous_token and previous_token.e_category in [ElementCategory.ANIME_SEASON,
                                                                ElementCategory.ANIME_SEASON_PREFIX]:
                token.t_category = TokenCategory.IDENTIFIER
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)

                is_found = True
                continue
            next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
            if next_token is None or next_token.t_category != TokenCategory.UNKNOWN:
                continue

            # Check if it's an isolated number
            if not self.is_token_isolated(next_token):
                continue
            if not next_token.content.isdigit():
                continue

            episode = min(token, next_token, key=lambda t: t.content)
            continue_episode = max(token, next_token, key=lambda t: t.content)

            self.set_token_element(episode, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            self.set_token_element(continue_episode, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
            is_found = True
        return is_found

    def search_for_isolated_numbers(self, tokens: List[Token]) -> bool:
        """
        Search for isolated numbers.
        """
        is_found = False
        for token in tokens:
            if not token.enclosed:
                continue
            if not self.is_token_isolated(token):
                continue
            if token.content.isdigit():
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)

                is_found = True
        return is_found

    def search_for_last_number(self, tokens: List[Token]) -> bool:
        """
        Search for the last number.
        """
        is_found = False
        for token in tokens:
            token_index = self.get_index(token)

            # assuming the episode number always come after the title
            if token_index == 0:
                continue

            if token.enclosed:
                continue

            # Ignore if it's the first non-enclosed, non-delimiter token
            if all([t.enclosed or t.t_category == TokenCategory.DELIMITER
                    for t in self.get_list()[:token_index]]):
                continue

            # Ignore if the previous token is "Movie" or "Part"
            previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
            if previous_token and str(previous_token.content).lower() in ["part"]:
                continue
            previous_token = self.find_prev(token, TokenFlags.UNKNOWN | TokenFlags.BRACKET)
            if not previous_token or previous_token == token:  # , because previous_token most likely same as token
                continue
            if not parser_helper.is_dash_character(previous_token.content):
                next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
                if next_token and parser_helper.is_dash_character(next_token.content):
                    try:
                        f_text = float(token.content)
                        if f_text.is_integer():
                            if str(int(f_text)) != token.content:
                                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                                is_found = True
                        elif str(f_text) != token.content:
                            self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                            is_found = True
                    except ValueError:
                        pass

                continue
            if token.content.isdigit():
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                is_found = True
        return is_found

    def search_for_number_patterns(self, tokens: List[Token]) -> bool:
        """
        Search for number patterns.
        """
        is_found = False
        for token in tokens:
            numeric_front = token.content[0].isdigit()

            if not numeric_front:
                # e.g. "EP.1", "Vol.1"
                if self.is_number_comes_after_prefix(token):
                    is_found = True
            elif self.is_number_comes_before_another_number(token):
                is_found = True

            if token.t_category == TokenCategory.UNKNOWN:
                # look for other patterns
                # if previous token is a dash, it is most likely an episode number
                prefix = False
                previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
                keyword = self.keyword_manager.find(
                    self.keyword_manager.normalize(previous_token.content))
                prev_is_dash = parser_helper.is_dash_character(previous_token.content)
                if prev_is_dash:
                    prefix = True
                else:
                    # in case the separator not a dash,
                    # we need to check if the next token are the same with the previous token
                    next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)

                    # the number are at the beginning of the string
                    if next_token:
                        next_is_dash = parser_helper.is_dash_character(next_token.content)
                        if (previous_token.content == next_token.content
                                or (previous_token == token and next_is_dash)
                                or (previous_token.t_category == next_token.t_category == TokenCategory.BRACKET
                                    and self.counter.get(ElementCategory.EPISODE_NUMBER))):
                            prefix = True
                    else:
                        # 02 is most likely an episode number
                        # but 2 is not guaranteed
                        try:
                            is_number = float(token.content)
                            if is_number.is_integer():
                                if str(int(is_number)) != token.content:
                                    prefix = True
                            else:
                                if str(is_number) != token.content:
                                    prefix = True
                        except ValueError:
                            # in case it 04v2, then it most likely an episode number
                            prefix = True

                    if not prefix:
                        if keyword and keyword.e_category == ElementCategory.ANIME_TYPE:
                            prefix = True

                if self.is_match_number_patterns(token, token.content, ElementCategory.EPISODE_NUMBER, prefix):
                    is_found = True
                    if prefix:
                        if keyword and keyword.e_category == ElementCategory.ANIME_TYPE:
                            self.set_token_element(previous_token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_TYPE)
        return is_found

    def search_for_seperated_numbers(self, tokens: List[Token]) -> bool:
        """
        Search for seperated numbers.
        """
        is_found = False
        for token in tokens:
            previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)

            if previous_token is None or previous_token.t_category != TokenCategory.UNKNOWN:
                continue

            if parser_helper.is_dash_character(previous_token.content) and token.content.isdigit():
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER)
                self.set_token_element(previous_token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX)

                is_found = True
        return is_found
