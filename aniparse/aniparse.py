import os

from aniparse.parser_option import Options
from aniparse.element import ElementCategory
from aniparse.parser import Parser


class Aniparse(Parser):
    def __init__(self, filename, options: Options, keywords_manager):
        self.options = options
        self.anime: dict = {}

        basename = self.remove_extension_from_filename(filename)
        cleaned_name = self.remove_ignored_strings_from_filename(basename)
        super().__init__(cleaned_name, options, keywords_manager)

    def remove_extension_from_filename(self, filename) -> str:
        """
        Get basename from filename and remove extension from filename
        :param filename:
        :return:
        """

        basename, extension = os.path.splitext(filename)

        if len(extension) > self.options.max_extension_length:
            return filename

        if extension:
            self.anime[ElementCategory.FILE_EXTENSION] = extension
        self.anime[ElementCategory.FILE_NAME] = basename
        return basename

    def remove_ignored_strings_from_filename(self, filename) -> str:
        for string in self.options.ignored_strings:
            filename = filename.replace(string, '')

        return filename
