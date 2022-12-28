import os

from aniparse.element import ElementCategory
from aniparse.parser import Parser


class Aniparse(Parser):
    """
    A class for parsing anime filenames and extracting relevant information.
    """
    def __init__(self, filename, options, keywords_manager):
        self.anime: dict = {
            ElementCategory.FILE_NAME.value: filename
        }

        super().__init__(filename, options, keywords_manager)

    def parse(self) -> None:
        """
        Parse the filename and extract the relevant information.
        """
        self.parse_video_extension()

        # Remove the ignored strings from the filename
        for ignored_string in self.options['ignored_strings']:
            self.filename = self.filename.replace(ignored_string, '')

        if not self.filename:
            return  # the anime is unknown
        super().parse()

    def populate(self) -> dict:
        """
        Populate the anime dictionary with the elements and tokens
        :return:
        """
        raise NotImplementedError

    def parse_video_extension(self) -> None:
        """
        Parse the video extension from the filename and store it in the anime dictionary.
        """
        filename, extension = os.path.splitext(self.filename)

        # Check if the extension is a valid video format
        if extension in self.options['valid_video_formats']:
            # Store the extension in the anime dictionary
            self.anime[ElementCategory.FILE_EXTENSION.value] = extension
        else:
            # Update the filename with the original value including the extension
            self.filename = self.anime[ElementCategory.FILE_NAME.value]

