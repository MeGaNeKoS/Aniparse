import enum
from typing import Collection


class Category(enum.Enum):
    """THis category is everything that available during pre-processing"""
    # Series-related elements
    TITLE = 'title'  # Official title of the series or movie
    TYPE = 'type'  # Type of series (e.g., TV Show, Anime, Movie)
    YEAR = 'year'  # Year the series started or movie was released

    # General context for scoring purpose
    SEQUENCE_PREFIX = 'sequence_prefix'  # A prefix to describe the sequence (e.g., "EP", "Part", "Volume", "Season",)
    SEQUENCE_NUMBER = 'sequence_number'  # The sequence number of the episode (e.g., "01", "02")
    SEQUENCE_PART = "sequence_part"  # C in OP2C
    SEQUENCE_RANGE = 'sequence_range'  # Sequence range token like "of", "&", "-"

    # File-related elements
    FILE_CHECKSUM = 'file_checksum'  # Checksum for the file
    FILE_INDEX = 'file_index'  # Index number of the file

    # Audio-related elements
    AUDIO_TERM = 'audio_term'  # Audio attributes (e.g., "Stereo", "5.1")

    # Release-related elements
    RELEASE_GROUP = 'release_group'  # Group responsible for the release
    RELEASE_INFORMATION = 'release_information'  # Additional information about the release
    RELEASE_VERSION = 'release_version'  # Version of the release
    RELEASE_VERSION_PREFIX = 'release_version_prefix'  # Prefix for the release version (e.g., "v", "Version")

    # Video-related elements
    VIDEO_RESOLUTION = 'video_resolution'  # Video resolution (e.g., "1080p", "720p")
    VIDEO_TERM = 'video_term'  # Video attributes (e.g., "HDR")
    SOURCE = 'source'  # Source of the video (e.g., "BluRay", "WEB-DL")

    # Subtitle-related elements
    SUBS_TERM = 'subs_term'  # Indicates presence of subtitles

    # Delimiter and formatting elements
    CONTEXT_DELIMITER = 'context_delimiter'  # Delimiter between contexts (e.g., "-", "_")
    BRACKET = 'bracket'  # Type of brackets used (e.g., "[]", "()")
    DELIMITER = 'delimiter'  # General delimiter (e.g., ".", " ")

    # Miscellaneous elements
    # The token where it requires another token or effect other token score. (E.g., "THE" near "END" or "FINAL)
    # The token where it extends the context of the token. (E.g., "+" between "EP01+02" or "EP01-02")
    CONTEXT_DEPENDENT = 'context_dependent'

    # Language and compatibility
    LANGUAGE = 'language'  # General/all detected language list.
    DEVICE_COMPATIBILITY = 'device_compatibility'  # Indicates device compatibility (e.g., "Mobile")
    EXTRA_INFO = 'extra_info'  # Any extra information or specialized info that rely on previous token

    # Undefined elements
    UNKNOWN = 'unknown'  # Any unknown elements in the filename

    def __contains__(self, item: 'Category') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value

    @classmethod
    def get_optional_info(cls) -> list['Category']:
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
    def additional_video_information(cls, items: Collection['Category']) -> bool:
        for item in items:
            if item in cls.get_optional_info():
                return True
        return False


class Descriptor(enum.Enum):
    """THis category is everything that available post-processing"""
    # Series-related elements
    SERIES_TITLE = 'series_title'  # Official title of the series or movie
    SERIES_TYPE = 'series_type'  # Type of series (e.g., TV Show, Anime, Movie)
    SERIES_YEAR = 'series_year'  # Year the series started or movie was released

    # Season/Episode/volume sequence-related elements
    SERIES = "series"
    SEASON = "season"
    EPISODE = "episode"
    VOLUME = "volume"
    CONTENT_TYPE = "content_type"
    CONTENT_IDENTIFIER = "content_identifier"  # PV, Preview, OP

    # General context for scoring purpose
    SEQUENCE_NUMBER = 'sequence_number'  # The sequence number of the episode (e.g., "01", "02")
    SEQUENCE_ALTERNATIVE = "sequence_alternative"
    SEQUENCE_PART = "sequence_part"  # C in OP2C
    SEQUENCE_TITLE = 'sequence_title'  # Title of the individual sequence
    SEQUENCE_TOTAL = "sequence_total"
    SEQUENCE_RANGE = 'sequence_range'  # Sequence range token like "of", "&", "-"
    SEQUENCE_START = 'sequence_start'
    SEQUENCE_END = 'sequence_end'

    # File-related elements
    FILE_NAME = 'file_name'  # Name of the file
    FILE_CHECKSUM = 'file_checksum'  # Checksum for the file
    FILE_EXTENSION = 'file_extension'  # File extension (e.g., ".mp4")
    FILE_INDEX = 'file_index'  # Index number of the file

    # Audio-related elements
    AUDIO_TERM = 'audio_term'  # Audio attributes (e.g., "Stereo", "5.1")

    # Release-related elements
    RELEASE_GROUP = 'release_group'  # Group responsible for the release
    RELEASE_INFORMATION = 'release_information'  # Additional information about the release
    RELEASE_VERSION = 'release_version'  # Version of the release
    RELEASE_VERSION_PREFIX = 'release_version_prefix'  # Prefix for the release version (e.g., "v", "Version")

    # Video-related elements
    VIDEO_RESOLUTION = 'video_resolution'  # Video resolution (e.g., "1080p", "720p")
    VIDEO_WIDTH = 'width'
    VIDEO_HEIGHT = 'height'
    SCAN_METHOD = 'scan_method'
    VIDEO_TERM = 'video_term'  # Video attributes (e.g., "HDR")
    SOURCE = 'source'  # Source of the video (e.g., "BluRay", "WEB-DL")

    # Subtitle-related elements
    SUBS_TERM = 'subs_term'  # Indicates presence of subtitles

    # Delimiter and formatting elements
    CONTEXT_DELIMITER = 'context_delimiter'  # Delimiter between contexts (e.g., "-", "_")
    BRACKET = 'bracket'  # Type of brackets used (e.g., "[]", "()")
    DELIMITER = 'delimiter'  # General delimiter (e.g., ".", " ")

    # Miscellaneous elements
    # The token where it requires another token or effect other token score. (E.g., "THE" near "END" or "FINAL)
    # The token where it extends the context of the token. (E.g., "+" between "EP01+02" or "EP01-02")
    CONTEXT_DEPENDENT = 'context_dependent'

    # Language and compatibility
    LANGUAGE = 'language'  # General/all detected language list.
    DEVICE_COMPATIBILITY = 'device_compatibility'  # Indicates device compatibility (e.g., "Mobile")
    EXTRA_INFO = 'extra_info'  # Any extra information not categorized

    # Undefined elements
    OTHER = 'other'  # Any other information
    UNKNOWN = 'unknown'  # Any unknown elements in the filename

    def __contains__(self, item: 'Descriptor') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value

    @classmethod
    def to_label(cls, item: 'Descriptor') -> 'Category':
        """Converts a Metadata item to a Label"""

        # Series Elements
        if item == cls.SERIES_TITLE:
            return Category.TITLE
        elif item == cls.SERIES_TYPE:
            return Category.TYPE
        elif item == cls.SERIES_YEAR:
            return Category.YEAR

        # Episode/Volume/Sequence Elements
        elif item in (cls.SEASON, cls.EPISODE, cls.VOLUME, cls.CONTENT_TYPE):
            return Category.SEQUENCE_PREFIX
        elif item == cls.SEQUENCE_NUMBER:
            return Category.SEQUENCE_NUMBER
        elif item == cls.SEQUENCE_PART:
            return Category.SEQUENCE_PART
        elif item == cls.SEQUENCE_TITLE:
            return Category.TITLE
        elif item == cls.SEQUENCE_TOTAL:
            return Category.SEQUENCE_NUMBER
        elif item == cls.SEQUENCE_RANGE:
            return Category.SEQUENCE_RANGE

        # File Elements
        elif item == cls.FILE_CHECKSUM:
            return Category.FILE_CHECKSUM
        elif item == cls.FILE_INDEX:
            return Category.FILE_INDEX

        # Audio Elements
        elif item == cls.AUDIO_TERM:
            return Category.AUDIO_TERM

        # Release Elements
        elif item == cls.RELEASE_GROUP:
            return Category.RELEASE_GROUP
        elif item == cls.RELEASE_INFORMATION:
            return Category.RELEASE_INFORMATION
        elif item == cls.RELEASE_VERSION:
            return Category.RELEASE_VERSION
        elif item == cls.RELEASE_VERSION_PREFIX:
            return Category.RELEASE_VERSION_PREFIX

        # Video Elements
        elif item == cls.VIDEO_RESOLUTION:
            return Category.VIDEO_RESOLUTION
        elif item in (cls.VIDEO_WIDTH, cls.VIDEO_HEIGHT):
            return Category.VIDEO_RESOLUTION
        elif item == cls.VIDEO_TERM:
            return Category.VIDEO_TERM
        elif item == cls.SOURCE:
            return Category.SOURCE

        # Subtitle Elements
        elif item == cls.SUBS_TERM:
            return Category.SUBS_TERM

        # Delimiters
        elif item == cls.CONTEXT_DELIMITER:
            return Category.CONTEXT_DELIMITER
        elif item == cls.BRACKET:
            return Category.BRACKET
        elif item == cls.DELIMITER:
            return Category.DELIMITER

        # Miscellaneous
        elif item == cls.CONTEXT_DEPENDENT:
            return Category.CONTEXT_DEPENDENT
        elif item == cls.LANGUAGE:
            return Category.LANGUAGE
        elif item == cls.DEVICE_COMPATIBILITY:
            return Category.DEVICE_COMPATIBILITY
        elif item == cls.EXTRA_INFO:
            return Category.EXTRA_INFO

        # Fallback
        return Category.UNKNOWN
