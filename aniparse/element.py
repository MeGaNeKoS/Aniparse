import enum


class ElementCategory(enum.Enum):
    ANIME_SEASON = 'anime_season'
    ANIME_SEASON_PREFIX = 'anime_season_prefix'
    ANIME_TITLE = 'anime_title'
    ANIME_TITLE_ALT = 'anime_title_alt'
    ANIME_TYPE = 'anime_type'
    ANIME_YEAR = 'anime_year'
    AUDIO_TERM = 'audio_term'
    DEVICE_COMPATIBILITY = 'device_compatibility'
    BRACKET = 'bracket'
    DELIMITER = 'delimiter'
    EPISODE_NUMBER = 'episode_number'
    EPISODE_PART = 'episode_part'
    EPISODE_NUMBER_ALT = 'episode_number_alt'
    EPISODE_PREFIX = 'episode_prefix'
    EPISODE_TITLE = 'episode_title'
    EPISODE_TOTAL = 'episode_total'
    FILE_CHECKSUM = 'file_checksum'
    FILE_EXTENSION = 'file_extension'
    FILE_NAME = 'file_name'
    LANGUAGE = 'language'
    OTHER = 'other'
    RANGE_SEPARATOR = 'range_separator'
    RELEASE_GROUP = 'release_group'
    RELEASE_INFORMATION = 'release_information'
    RELEASE_VERSION = 'release_version'
    SOURCE = 'source'
    SUBTITLES = 'subtitles'
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
        return self.value == item.value
