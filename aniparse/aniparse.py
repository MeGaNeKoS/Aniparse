import re

from aniparse import parser_helper
from aniparse.element import ElementCategory
from aniparse.parser import Parser
from aniparse.token import TokenCategory


class Aniparse(Parser):
    def __init__(self, filename, options, keywords_manager):
        self.anime: dict = {
            ElementCategory.FILE_NAME.value: filename
        }

        super().__init__(filename, options, keywords_manager)

    def parse(self) -> None:
        """
        Parse the filename, getting the elements and tokens
        :return:
        """
        self.remove_extension_from_filename()

        self.remove_ignored_strings_from_filename()

        if not self.filename:
            self.anime = None
            return  # the anime is unknown
        super().parse()

    def populate(self) -> dict:
        """
        Populate the anime dictionary with the elements and tokens
        :return:
        """
        for token in self.tokens:
            element = token.e_category
            if token.t_category == TokenCategory.INVALID:
                continue

            if token.t_category == TokenCategory.BRACKET:
                continue
            if token.t_category == TokenCategory.DELIMITER:
                continue

            if token.t_category == TokenCategory.UNKNOWN or element == ElementCategory.UNKNOWN:
                element = ElementCategory.OTHER

            if self.options["ignored_dash"]:
                if parser_helper.is_dash_character(token.content):
                    continue

            if element in [
                ElementCategory.ANIME_SEASON,
                ElementCategory.ANIME_YEAR,
                ElementCategory.EPISODE_NUMBER,
                ElementCategory.EPISODE_NUMBER_ALT,
                ElementCategory.EPISODE_TOTAL,
                ElementCategory.RELEASE_VERSION,
                ElementCategory.VOLUME_NUMBER
            ]:
                # set the content to be a number, or float if it has a decimal
                try:
                    token.content = int(token.content)
                except ValueError:
                    token.content = float(token.content)

            # if the element already in the dictionary, transform it into a list and append the new value
            element = element.value
            if element in self.anime:
                if not isinstance(self.anime[element], list):
                    self.anime[element] = [self.anime[element]]
                self.anime[element].append(token.content)
            else:
                self.anime[element] = token.content
        # clean up the anime dictionary
        for element in [ElementCategory.ANIME_TITLE,
                        ElementCategory.ANIME_TITLE_ALT,
                        ElementCategory.EPISODE_TITLE]:
            value = element.value
            if isinstance(self.anime.get(value, None), list):
                string = "".join(self.anime[value]).strip(
                    " " + parser_helper.DASHES if self.options["ignored_dash"] else "")  # any similar dash
            elif isinstance(self.anime.get(value, None), str):
                string = self.anime.get(value, "")
            else:
                continue
            # remove double spaces
            string = re.sub(r"\s+", " ", string)
            if string.isspace():
                self.anime.pop(value)
            else:
                self.anime[value] = string

        return self.anime

    def remove_extension_from_filename(self) -> None:
        split_filename = self.filename.rsplit('.', 1)

        if len(split_filename) < 2:
            return

        new_filename, extension = split_filename

        if len(extension) > self.options['max_extension_length']:
            return

        # normalize the extension and check if it is a valid extension
        keyword = self.keyword_manager.normalize(extension)
        # only return if the extension is a valid video extension
        if not self.keyword_manager.find(keyword, ElementCategory.FILE_EXTENSION):
            return

        if extension:
            self.anime[ElementCategory.FILE_EXTENSION.value] = extension
        self.filename = new_filename

    def remove_ignored_strings_from_filename(self) -> None:
        for string in self.options["ignored_strings"]:
            self.filename = self.filename.replace(string, '')

