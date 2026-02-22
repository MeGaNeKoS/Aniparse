import enum
from typing import Collection


class Tag(enum.Enum):
    """Single enum for all token tagging — both scoring keys and fine-grained descriptors."""

    # Series-related
    TITLE = 'title'
    TYPE = 'type'
    YEAR = 'year'
    SERIES_TITLE = 'series_title'
    SERIES_TYPE = 'series_type'
    SERIES_YEAR = 'series_year'

    # Sequence prefix (scoring group for SEASON/EPISODE/VOLUME/etc.)
    SEQUENCE_PREFIX = 'sequence_prefix'
    SERIES = 'series'
    SEASON = 'season'
    EPISODE = 'episode'
    VOLUME = 'volume'
    CONTENT_TYPE = 'content_type'
    CONTENT_IDENTIFIER = 'content_identifier'

    # Sequence numbers and ranges
    SEQUENCE_NUMBER = 'sequence_number'
    SEQUENCE_ALTERNATIVE = 'sequence_alternative'
    SEQUENCE_PART = 'sequence_part'
    SEQUENCE_TITLE = 'sequence_title'
    SEQUENCE_TOTAL = 'sequence_total'
    SEQUENCE_RANGE = 'sequence_range'
    SEQUENCE_START = 'sequence_start'
    SEQUENCE_END = 'sequence_end'

    # File-related
    FILE_NAME = 'file_name'
    FILE_CHECKSUM = 'file_checksum'
    FILE_EXTENSION = 'file_extension'
    FILE_INDEX = 'file_index'

    # Audio-related
    AUDIO_TERM = 'audio_term'

    # Release-related
    RELEASE_GROUP = 'release_group'
    RELEASE_INFORMATION = 'release_information'
    RELEASE_VERSION = 'release_version'
    RELEASE_VERSION_PREFIX = 'release_version_prefix'

    # Video-related
    VIDEO_RESOLUTION = 'video_resolution'
    VIDEO_WIDTH = 'width'
    VIDEO_HEIGHT = 'height'
    SCAN_METHOD = 'scan_method'
    VIDEO_TERM = 'video_term'
    SOURCE = 'source'

    # Subtitle-related
    SUBS_TERM = 'subs_term'

    # Delimiter and formatting
    CONTEXT_DELIMITER = 'context_delimiter'
    BRACKET = 'bracket'
    DELIMITER = 'delimiter'

    # Miscellaneous
    CONTEXT_DEPENDENT = 'context_dependent'

    # Language and compatibility
    LANGUAGE = 'language'
    DEVICE_COMPATIBILITY = 'device_compatibility'
    EXTRA_INFO = 'extra_info'

    # Undefined
    OTHER = 'other'
    UNKNOWN = 'unknown'

    def __contains__(self, item: 'Tag') -> bool:
        return self.value == item.value

    @property
    def group(self) -> 'Tag':
        """Return the scoring-group head for this tag.

        Most tags map to themselves. Fine-grained tags (SEASON, EPISODE, etc.)
        collapse into coarser group heads (SEQUENCE_PREFIX, TITLE, etc.).
        """
        return _GROUP_OVERRIDES.get(self, self)

    @classmethod
    def get_optional_info(cls) -> list['Tag']:
        return [
            cls.FILE_CHECKSUM,
            cls.AUDIO_TERM,
            cls.RELEASE_GROUP,
            cls.RELEASE_INFORMATION,
            cls.RELEASE_VERSION,
            cls.RELEASE_VERSION_PREFIX,
            cls.VIDEO_RESOLUTION,
            cls.VIDEO_TERM,
            cls.SOURCE,
            cls.SUBS_TERM,
            cls.LANGUAGE,
            cls.DEVICE_COMPATIBILITY,
            cls.EXTRA_INFO,
        ]

    @classmethod
    def additional_video_information(cls, items: Collection['Tag']) -> bool:
        for item in items:
            if item in cls.get_optional_info():
                return True
        return False


# Many-to-one overrides: fine-grained tag → scoring group head
_GROUP_OVERRIDES = {
    Tag.SERIES_TITLE: Tag.TITLE,
    Tag.SERIES_TYPE: Tag.TYPE,
    Tag.SERIES_YEAR: Tag.YEAR,
    Tag.SEASON: Tag.SEQUENCE_PREFIX,
    Tag.EPISODE: Tag.SEQUENCE_PREFIX,
    Tag.VOLUME: Tag.SEQUENCE_PREFIX,
    Tag.CONTENT_TYPE: Tag.SEQUENCE_PREFIX,
    Tag.SEQUENCE_TITLE: Tag.TITLE,
    Tag.SEQUENCE_TOTAL: Tag.SEQUENCE_NUMBER,
    Tag.VIDEO_WIDTH: Tag.VIDEO_RESOLUTION,
    Tag.VIDEO_HEIGHT: Tag.VIDEO_RESOLUTION,
}
