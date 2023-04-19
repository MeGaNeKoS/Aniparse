import enum


class ElementCategory(enum.Enum):
    """
    An enumeration of the different categories of elements that can appear in an anime filename.
    """
    ANIME_SEASON = 'anime_season_prefix.txt'
    ANIME_SEASON_PREFIX = 'anime_season_prefix.txt'
    ANIME_TITLE = 'anime_title'
    ANIME_TITLE_ALT = 'anime_title_alt'
    ANIME_TYPE = 'anime_type'
    ANIME_YEAR = 'anime_year'
    AUDIO_TERM = 'audio_term'
    BATCH = 'batch'
    CONTEXT_DELIMITER = 'context_delimiter'
    CREDIT_NUMBER = 'credit_number'
    DEVICE_COMPATIBILITY = 'device_compatibility'
    BRACKET = 'bracket'
    DELIMITER = 'delimiter'
    DELIMITER_IN_GROUP = 'delimiter_in_group'
    EPISODE_NUMBER = 'episode_number'
    EPISODE_NUMBER_ALT = 'episode_number_alt'
    EPISODE_PART = 'episode_part'
    EPISODE_PREFIX = 'episode_prefix'
    EPISODE_TITLE = 'episode_title'
    EPISODE_TOTAL = 'episode_total'
    EXTRA_INFO = 'extra_info'
    FILE_CHECKSUM = 'file_checksum'
    FILE_EXTENSION = 'file_extension'
    FILE_NAME = 'file_name'
    FILE_INDEX = 'file_index'
    FILE_TYPE = 'file_type'
    LANGUAGE = 'language'
    OTHER = 'other'
    RANGE_SEPARATOR = 'range_separator'
    RELEASE_GROUP = 'release_group'
    RELEASE_INFORMATION = 'release_information'
    RELEASE_VERSION = 'release_version'
    RELEASE_PREFIX = 'release_prefix'
    SOURCE = 'source'
    SUBTITLES = 'subtitles'
    SUBTITLE_TYPE = 'subtitle_type'
    VIDEO_RESOLUTION = 'video_resolution'
    VIDEO_TERM = 'video_term'
    VOLUME_NUMBER = 'volume_number'
    VOLUME_PREFIX = 'volume_prefix'
    UNKNOWN = 'unknown'

    @classmethod
    def is_searchable(cls, category: 'ElementCategory') -> bool:
        searchable_categories = [
            cls.ANIME_SEASON_PREFIX,
            cls.ANIME_TYPE,
            cls.AUDIO_TERM,
            cls.DEVICE_COMPATIBILITY,
            cls.EPISODE_PREFIX,
            cls.FILE_CHECKSUM,
            cls.LANGUAGE,
            cls.OTHER,
            cls.RELEASE_GROUP,
            cls.RELEASE_INFORMATION,
            cls.RELEASE_VERSION,
            cls.SOURCE,
            cls.SUBTITLES,
            cls.VIDEO_RESOLUTION,
            cls.VIDEO_TERM,
            cls.VOLUME_PREFIX
        ]
        return category in searchable_categories

    def __contains__(self, item: 'ElementCategory') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value




