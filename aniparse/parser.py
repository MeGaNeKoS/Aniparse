import logging

from aniparse import parser_helper, parser_number
from aniparse.element import ElementCategory
from aniparse.parser_number import ParserNumber
from aniparse.token import TokenCategory, TokenFlags, Token
from aniparse.tokenizer import Tokenizer

logger = logging.getLogger(__name__)


class Parser(Tokenizer, ParserNumber):

    def build_element(self, e_category: ElementCategory, token_begin=None, token_end=None) -> None:
        """
        Set the element category for all tokens between token_begin and token_end.

        :param e_category:
        :param token_begin:
        :param token_end:
        :return:
        """
        for token in self.get_list(begin=token_begin, end=token_end):
            if token.t_category == TokenCategory.UNKNOWN:
                self.set_token_element(token, TokenCategory.IDENTIFIER, e_category)
            elif token.t_category == TokenCategory.BRACKET:
                self.set_token_element(token, TokenCategory.IDENTIFIER, e_category)
            elif token.t_category == TokenCategory.DELIMITER:
                delimiter = token.content
                if self.options['keep_delimiters']:
                    self.set_token_element(token, TokenCategory.DELIMITER, e_category)
                elif token != token_begin and token != token_end:
                    if delimiter == ',' or delimiter == '&':
                        self.set_token_element(token, TokenCategory.IDENTIFIER, e_category)
                    else:
                        token.content = " "
                        self.set_token_element(token, TokenCategory.IDENTIFIER, e_category)
            else:
                self.set_token_element(token, TokenCategory.IDENTIFIER, e_category)

    def is_anime_season_keyword(self, token) -> bool:
        """
        Check if the token is a season keyword.
        :param token:
        :return:
        """
        # check for tre previous tokens
        previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
        if previous_token:
            number = parser_helper.get_number_from_ordinal(previous_token.content)
            if number:
                self.set_token_element(previous_token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
                previous_token.content = number
                return True

        # check for the next token
        next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
        if next_token:
            if next_token.content.isdigit():
                self.set_token_element(next_token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON)
                return True
        return False

    def parse(self) -> None:
        """
        Parse the tokens.
        First, the tokens are categorized. Then, find the indentifiable and searchable keyword.
        After that, look for isolated number for the year and video resolution. Finally, look for episode number.
        Once we have that information, we can determine the anime title, and episode title.
        Lastly, we can check for the release group and validate the elements.
        Any UNKNOWN token will be set to OTHER's category.
        :return:
        """
        if not self.tokenize():
            return None

        self.search_for_keywords()  # search for unique keywords for [year, video resolution, crc32, etc]

        self.search_for_isolated_number()  # search for isolated numbers for [season, anime year]

        self.search_for_episode_number()  # search for episode number. If it not exist, then it can't have episode

        first_number = None
        last_number = None
        if self.counter.get(ElementCategory.EPISODE_NUMBER, 0) == 2:
            first_number = self.find_next(None, element=ElementCategory.EPISODE_NUMBER)
            last_number = self.find_next(first_number, element=ElementCategory.EPISODE_NUMBER)
        elif self.counter.get(ElementCategory.VOLUME_NUMBER, 0) == 2:
            first_number = self.find_next(None, element=ElementCategory.VOLUME_NUMBER)
            last_number = self.find_next(first_number, element=ElementCategory.VOLUME_NUMBER)
        if first_number and last_number:
            tokens = list(self.get_list(flags=TokenFlags.UNKNOWN, begin=first_number, end=last_number))
            if len(tokens) == 1:
                if tokens[0].content in "&":
                    self.set_token_element(tokens[0], TokenCategory.INVALID, ElementCategory.RANGE_SEPARATOR)

        self.search_for_anime_title()

        self.search_for_episode_title()

        self.search_for_release_group()

        self.validate_elements()

    def search_for_anime_title(self) -> None:
        """
        Search for the anime title.
        First, we find not enclosed or unknown tokens. If we don't find any, then we
        check if `check_title_enclosed` is True. If it is, then we check for enclosed tokens.
        After that, we verify there is no Anime season, season prefix, episode number, volume number,
        or anime type before the anime title if `title_before_episode` is True.
        Finally, we can search the token_end for the anime title until it found an IDENTIFIER or BRACKET token.

        :return:
        """
        enclosed_title = False

        token_begin = self.find(TokenFlags.NOT_ENCLOSED | TokenFlags.UNKNOWN)
        if token_begin is None:
            if self.options['check_title_enclosed']:
                enclosed_title = True
                token_begin = self.get(0)
                skipped_previous_group = False

                while token_begin is not None:
                    token_begin = self.find_next(token_begin, TokenFlags.UNKNOWN | TokenFlags.IDENTIFIER)
                    if token_begin is None:
                        break

                    if (token_begin.e_category == ElementCategory.ANIME_SEASON_PREFIX
                            or token_begin.e_category == ElementCategory.ANIME_SEASON
                            or token_begin.e_category == ElementCategory.EPISODE_PREFIX
                            or token_begin.e_category == ElementCategory.EPISODE_NUMBER
                            or token_begin.e_category == ElementCategory.ANIME_TYPE):
                        if self.options['title_before_episode']:
                            break
                        else:
                            continue
                    # Ignore groups that are composed of non-Latin characters
                    if parser_helper.is_mostly_latin_string(token_begin.content):
                        if skipped_previous_group:
                            break  # Found it
                    # Get the first unknown token of the next group
                    token_begin = self.find_next(token_begin, TokenFlags.BRACKET)
                    skipped_previous_group = True

        if token_begin is None:
            return

        # if we see season prefix, number, or episode prefix, number, before token begin,
        # the stop searching for anime title
        for token in self.get_list(end=token_begin):
            if (self.options['title_before_episode']
                    and (token.e_category == ElementCategory.ANIME_SEASON_PREFIX
                         or token.e_category == ElementCategory.ANIME_SEASON
                         or token.e_category == ElementCategory.EPISODE_PREFIX
                         or token.e_category == ElementCategory.EPISODE_NUMBER
                         or token.e_category == ElementCategory.ANIME_TYPE)):
                return

        token_end = self.find_next(token_begin, TokenFlags.IDENTIFIER | (
            TokenFlags.BRACKET if enclosed_title else TokenFlags.NONE
        ))

        # If within the interval there's an open bracket without its matching
        # pair, move the upper endpoint back to the bracket
        if not enclosed_title:
            last_bracket = token_end
            bracket_open = False
            for token in self.get_list(TokenFlags.BRACKET, begin=token_begin, end=token_end):
                last_bracket = token
                bracket_open = not bracket_open
            if bracket_open:
                token_end = last_bracket

        # If the interval ends with an enclosed group (e.g. "Anime Title
        # [Fansub]"), move the upper endpoint back to the beginning of the
        # group. We ignore parentheses in order to keep certain groups (e.g.
        # "(TV)") intact.
        if not enclosed_title:
            token = self.find_prev(token_end, TokenFlags.NOT_DELIMITER)
            while token.t_category == TokenCategory.BRACKET and token.content != ")":
                token = self.find_prev(token, TokenFlags.BRACKET)
                if token is not None:
                    token_end = token
                    token = self.find_prev(token_end, TokenFlags.NOT_DELIMITER)
            # Not sure why this is here, but it breaks the parser if not here
            token_end = self.find_prev(token_end, TokenFlags.VALID)

        for token in self.get_list(begin=token_begin, end=token_end):
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(token.content))
            if keyword:
                element = keyword.e_category
                if element == ElementCategory.ANIME_TYPE:
                    if token.content.upper() in ["ED", "NCED", "ENDING", "CLEAN ENDING",
                                                 "OP", "NCOP", "OPENING", "CLEAN OPENING"]:
                        break
                    previous_token = self.find_prev(token, TokenFlags.NOT_DELIMITER)
                    if previous_token and parser_helper.is_dash_character(previous_token.content):
                        next_token = self.find_next(token, TokenFlags.NOT_DELIMITER)
                        if next_token:
                            if next_token.t_category != TokenCategory.UNKNOWN:
                                break
                        else:
                            break
            token_end = token
        if enclosed_title:
            token_end = self.find_prev(token_end, TokenFlags.VALID)
        self.build_element(ElementCategory.ANIME_TITLE, token_begin,
                           token_end)

    def search_for_episode_number(self) -> None:
        """
        Search for the episode number.
        First, we get all tokens that have number in it, Then we check for number pattern, buggy dash, equivalent number,
        seperated number, isolated number, and finally, last number as the last resort.
        :return:
        """
        tokens = []
        for token in self.get_list(TokenFlags.UNKNOWN):
            if parser_helper.find_number_in_string(token.content) is None:
                continue
            tokens.append(token)

        if not tokens:
            return

        if self.search_for_number_patterns(tokens):
            return

        tokens_original = tokens.copy()
        tokens = [token for token in tokens if token.content.isdigit()]

        if not tokens:
            # buggy dash, e.g. "Gunbuster-ep1"
            self.search_for_buggy_dash(tokens_original)
            return

        # e.g. "01 (176)", "29 (04)"
        if self.search_for_equivalent_numbers(tokens):
            return

        # e.g. " - 08"
        if self.search_for_seperated_numbers(tokens):
            return

        # e.g. "[12]", "(2006)"
        if self.search_for_isolated_numbers(tokens):
            return

        # consider using the last number as a last resort
        if self.search_for_last_number(tokens):
            return

    def search_for_episode_title(self) -> None:
        """
        Search for the episode title.
        First, We find the UNKNOWN or NOT_ENCLOSED token. Then, we makesure there's no Audio/Video/Resolution/Source
        before the token begin. After that, we find the IDENTIFIER or ENCLOSED token for token end.
        :return:
        """
        token_end = None
        for _ in range(len(self.tokens)):

            # Find the first non-enclosed unknown token
            if token_end:
                token_begin = self.find_next(
                    token_end, TokenFlags.NOT_ENCLOSED | TokenFlags.UNKNOWN)
            else:
                token_begin = self.find(
                    TokenFlags.NOT_ENCLOSED | TokenFlags.UNKNOWN)

            if token_begin is None:
                return
            if token_begin.t_category == TokenCategory.IDENTIFIER:
                continue
            breaking = False
            for token in self.get_list(end=token_begin):
                # return if token before token_begin is Video Resolution, Audio Term, Video Term, etc
                if token.e_category in [
                    ElementCategory.AUDIO_TERM,
                    ElementCategory.DEVICE_COMPATIBILITY,
                    ElementCategory.FILE_CHECKSUM,
                    ElementCategory.FILE_EXTENSION,
                    ElementCategory.FILE_NAME,
                    ElementCategory.LANGUAGE,
                    ElementCategory.OTHER,
                    ElementCategory.RELEASE_INFORMATION,
                    ElementCategory.SOURCE,
                    ElementCategory.SUBTITLES,
                    ElementCategory.VIDEO_RESOLUTION,
                    ElementCategory.VIDEO_TERM
                ]:
                    breaking = True
                    break
            if breaking:
                break

            if self.counter.get(ElementCategory.EPISODE_NUMBER, 0) == 1:
                for token in self.get_list(begin=token_begin):
                    if token.e_category in [
                        ElementCategory.ANIME_SEASON,
                        ElementCategory.ANIME_SEASON_PREFIX,
                        ElementCategory.ANIME_TITLE,
                        ElementCategory.ANIME_TITLE_ALT,
                        ElementCategory.EPISODE_NUMBER,
                        ElementCategory.EPISODE_PREFIX,
                        ElementCategory.EPISODE_PART,
                        ElementCategory.EPISODE_TOTAL,
                    ]:
                        breaking = True
                        break

            # Continue until a bracket or identifier is found
            token_end = self.find_next(
                token_begin, TokenFlags.BRACKET | TokenFlags.IDENTIFIER)
            if breaking:
                continue

            # Ignore if it's only a dash
            if self.distance(token_begin, token_end) <= 2 and \
                    parser_helper.is_dash_character(token_begin.content):
                continue

            # If token end is a bracket, then we get the previous token to be
            # included in the element
            if token_end and token_end.t_category == TokenCategory.BRACKET:
                token_end = self.find_prev(token_end, TokenFlags.VALID)
            # Build episode title
            self.build_element(
                ElementCategory.EPISODE_TITLE, token_begin, token_end)
        return

    def search_for_isolated_number(self) -> None:
        """
        This function will search for isolated number for the year and video resolution.
        :return:
        """
        for token in self.get_list(TokenFlags.UNKNOWN):
            if (not token.content.isdigit()
                    or not self.is_token_isolated(token)):
                continue

            number = int(token.content)
            if parser_number.ANIME_YEAR_MIN <= number <= parser_number.ANIME_YEAR_MAX:
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_YEAR)
            elif number == 480 or number == 720 or number == 1080 or number == 2160:
                self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.VIDEO_RESOLUTION)

    def search_for_keywords(self) -> None:
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
        for token in self.get_list(TokenFlags.UNKNOWN):
            word = token.content
            word = word.strip(' -')

            if not word:
                continue

            # skip if it is a number and not a CRC number
            if word.isdigit() and len(word) != 8:
                continue

            element = ElementCategory.UNKNOWN
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(word))
            if keyword:
                element = keyword.e_category

                if not ElementCategory.is_searchable(element):
                    continue
                if not keyword.options.searchable:
                    continue
                if not keyword.options.identifiable and not token.enclosed:
                    continue

                if (element == ElementCategory.ANIME_SEASON_PREFIX
                        and self.is_anime_season_keyword(token)):

                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_SEASON_PREFIX)

                elif (element == ElementCategory.EPISODE_PREFIX
                      and keyword.options.valid):
                    if self.is_extent_keyword(token, ElementCategory.EPISODE_NUMBER, prefix=True):
                        self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_PREFIX)

                elif element == ElementCategory.VOLUME_PREFIX:
                    if self.is_extent_keyword(token, ElementCategory.VOLUME_NUMBER, prefix=True):
                        self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.VOLUME_PREFIX)
                elif element == ElementCategory.RELEASE_VERSION:
                    # this is probably a version number
                    token.content = word[0]
                    self.set_token_element(token, TokenCategory.INVALID, ElementCategory.UNKNOWN)
                    new_token = Token(word[1:], TokenCategory.IDENTIFIER, ElementCategory.RELEASE_VERSION,
                                      token.enclosed)
                    self.insert_after(token, new_token)
                    continue
                elif element == ElementCategory.AUDIO_TERM:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.AUDIO_TERM)
                    continue
                elif element == ElementCategory.DEVICE_COMPATIBILITY:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.DEVICE_COMPATIBILITY)
                    continue
                elif element == ElementCategory.LANGUAGE:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.LANGUAGE)
                    continue
                elif element == ElementCategory.OTHER:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.OTHER)
                    continue
                elif element == ElementCategory.RELEASE_INFORMATION:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.RELEASE_INFORMATION)
                    continue
                elif element == ElementCategory.SOURCE:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.SOURCE)
                    continue
                elif element == ElementCategory.SUBTITLES:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.SUBTITLES)
                    continue
                elif element == ElementCategory.VIDEO_TERM:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.VIDEO_TERM)
                    continue

                # last resort to avoid false positives
                if token.enclosed:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, element)
                else:
                    continue
            else:
                # we could have multiple valid crc and resolution keywords.
                if parser_helper.is_crc32(word):
                    element = ElementCategory.FILE_CHECKSUM
                if parser_helper.is_resolution(word):
                    element = ElementCategory.VIDEO_RESOLUTION

            if element != ElementCategory.UNKNOWN:
                if keyword is None or keyword.options.identifiable:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, element)

    def search_for_release_group(self) -> None:
        """
        This function will search for the release group.
        It just look for the first UNKNOWN token that is enclosed.
        :return:
        """
        token_end = None
        for _ in range(len(self.tokens)):
            if token_end:
                token_begin = self.find_next(token_end, TokenFlags.UNKNOWN)
            else:
                token_begin = self.find(TokenFlags.UNKNOWN)
            if token_begin is None:
                return

            # Continue until a bracket or identifier is found
            token_end = self.find_next(token_begin, TokenFlags.BRACKET | TokenFlags.IDENTIFIER)
            if token_end is None:
                return

            if token_end.t_category != TokenCategory.BRACKET:
                continue

            # Ignore if it's not the first non-delimiter token in group
            previous_token = self.find_prev(token_begin, TokenFlags.NOT_DELIMITER)
            if previous_token is not None and previous_token.t_category != TokenCategory.BRACKET:
                continue

            # Build release group, token end is a bracket, so we get the
            # previous token to be included in the element
            token_end = self.find_prev(token_end, TokenFlags.VALID)
            # get all tokens between token_begin and token_end
            tokens = self.get_list(begin=token_begin, end=token_end)
            content = "".join(token.content for token in tokens)
            replaced_token = Token(content, TokenCategory.IDENTIFIER, ElementCategory.RELEASE_GROUP, TokenFlags.NONE)
            index = self.get_index(token_begin)
            for token in tokens:
                self.remove_token(token)
            self.insert(index, replaced_token)
            return

    def validate_elements(self) -> None:
        """
        This function will validate the elements.
        It will check the episode number for the episode number alternatives.
        Then it will check for the episode title, to avoid anime type end up as episode title and some identifier token.
        And finally it check for anime title in case it ends with `the` and have anime type. (e.g. `the movie`)
        :return:
        """
        if self.counter.get(ElementCategory.EPISODE_NUMBER, 0) > 1:
            # get last episode number token
            token_episode = self.find_prev(None, flags=TokenFlags.IDENTIFIER, element=ElementCategory.EPISODE_NUMBER)
            token_start_episode = self.find_next(None, flags=TokenFlags.IDENTIFIER,
                                                 element=ElementCategory.EPISODE_NUMBER)
            token_start = self.find_next(token_start_episode, flags=TokenFlags.MASK_CATEGORIES)

            tokens = self.get_list(begin=token_start, end=token_episode)

            for token in tokens:
                if token.e_category == ElementCategory.RANGE_SEPARATOR:
                    break
                if token.e_category == ElementCategory.EPISODE_NUMBER:
                    if float(token_start_episode.content) == float(token.content):
                        self.remove_token(token)
                        break

                    if self.options['eps_lower_than_alt']:
                        if float(token_start_episode.content) > float(token.content):
                            token = token_start_episode

                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.EPISODE_NUMBER_ALT)
                    break

        # Fill the unknown tokens with the keywords
        for token in self.get_list(TokenFlags.UNKNOWN):
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(token.content))
            if keyword:
                self.set_token_element(token, TokenCategory.IDENTIFIER, keyword.e_category)

        # make sure there's no anime type in the episode title
        tokens = self.get_list(elements=ElementCategory.EPISODE_TITLE)
        is_other = False
        for token in tokens:
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(token.content))
            if keyword:
                if keyword.options.identifiable:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, keyword.e_category)
                    is_other = True
                elif is_other:
                    self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.OTHER)

        tokens = self.get_list(elements=ElementCategory.EPISODE_TITLE)
        real_token = []
        for token in tokens:
            if parser_helper.is_dash_character(token.content):
                continue
            if token.t_category in [TokenCategory.DELIMITER, TokenCategory.BRACKET]:
                continue
            real_token.append(token)

        if len(real_token) == 1:
            keyword = self.keyword_manager.find(self.keyword_manager.normalize(real_token[0].content))
            if keyword:
                self.set_token_element(real_token[0], TokenCategory.IDENTIFIER, keyword.e_category)

        token = self.find_prev(None, flags=TokenFlags.IDENTIFIER, element=ElementCategory.ANIME_TITLE)
        if token:
            if token.content.lower() == "the":
                anime_type = self.find_next(token, flags=TokenFlags.IDENTIFIER, element=ElementCategory.ANIME_TYPE)
                if anime_type:
                    tokens = self.get_list(begin=token, end=anime_type)
                    for token in tokens:
                        if token.t_category == TokenCategory.DELIMITER:
                            token.content = " "
                        self.set_token_element(token, TokenCategory.IDENTIFIER, ElementCategory.ANIME_TITLE)