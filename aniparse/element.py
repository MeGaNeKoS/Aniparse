import enum
from typing import Collection


class Label(enum.Enum):
    """THis category is everything that available during pre-processing"""
    # Series-related elements
    SERIES_TITLE = 'series_title'  # Official title of the series or movie
    SERIES_TYPE = 'series_type'  # Type of series (e.g., TV Show, Anime, Movie)
    SERIES_YEAR = 'series_year'  # Year the series started or movie was released

    # General context for scoring purpose
    SEQUENCE_PREFIX = 'sequence_prefix'  # A prefix to describe the sequence (e.g., "EP", "Part", "Volume", "Season",)
    SEQUENCE_NUMBER = 'sequence_number'  # The sequence number of the episode (e.g., "01", "02")
    SEQUENCE_PART = "sequence_part"  # C in OP2C
    SEQUENCE_TITLE = 'sequence_title'  # Title of the individual sequence
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
    EXTRA_INFO = 'extra_info'  # Any extra information not categorized

    # Undefined elements
    UNKNOWN = 'unknown'  # Any unknown elements in the filename

    def __contains__(self, item: 'Label') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value

    @classmethod
    def get_optional_info(cls) -> list['Label']:
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
    def additional_video_information(cls, items: Collection['Label']) -> bool:
        for item in items:
            if item in cls.get_optional_info():
                return True
        return False


class Metadata(enum.Enum):
    """THis category is everything that available post-processing"""
    # Series-related elements
    SERIES_TITLE = 'series_title'  # Official title of the series or movie
    SERIES_TYPE = 'series_type'  # Type of series (e.g., TV Show, Anime, Movie)
    SERIES_YEAR = 'series_year'  # Year the series started or movie was released

    MAIN = "main"
    ALT = "alt"
    # Season/Episode/volume sequence-related elements
    SEASON_PREFIX = "season"
    EPISODE_PREFIX = "episode"
    VOLUME_PREFIX = "volume"

    # General context for scoring purpose
    SEQUENCE_NUMBER = 'sequence_number'  # The sequence number of the episode (e.g., "01", "02")
    SEQUENCE_PART = "sequence_part"  # C in OP2C
    SEQUENCE_TITLE = 'sequence_title'  # Title of the individual sequence
    SEQUENCE_TOTAL = "sequence_total"
    SEQUENCE_RANGE = 'sequence_range'  # Sequence range token like "of", "&", "-"
    SEQUENCE_FROM = 'from'
    SEQUENCE_TO = 'to'

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

    def __contains__(self, item: 'Label') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value

    @classmethod
    def to_label(cls, item: 'Metadata') -> 'Label':
        """Converts a Metadata item to a Label"""

        # Series Elements
        if item == cls.SERIES_TITLE:
            return Label.SERIES_TITLE
        elif item == cls.SERIES_TYPE:
            return Label.SERIES_TYPE
        elif item == cls.SERIES_YEAR:
            return Label.SERIES_YEAR

        # Episode/Volume/Sequence Elements
        elif item in (cls.SEASON_PREFIX, cls.EPISODE_PREFIX, cls.VOLUME_PREFIX):
            return Label.SEQUENCE_PREFIX
        elif item == cls.SEQUENCE_NUMBER:
            return Label.SEQUENCE_NUMBER
        elif item == cls.SEQUENCE_PART:
            return Label.SEQUENCE_PART
        elif item == cls.SEQUENCE_TITLE:
            return Label.SEQUENCE_TITLE
        elif item == cls.SEQUENCE_TOTAL:
            return Label.SEQUENCE_NUMBER
        elif item == cls.SEQUENCE_RANGE:
            return Label.SEQUENCE_RANGE

        # File Elements
        elif item == cls.FILE_CHECKSUM:
            return Label.FILE_CHECKSUM
        elif item == cls.FILE_INDEX:
            return Label.FILE_INDEX

        # Audio Elements
        elif item == cls.AUDIO_TERM:
            return Label.AUDIO_TERM

        # Release Elements
        elif item == cls.RELEASE_GROUP:
            return Label.RELEASE_GROUP
        elif item == cls.RELEASE_INFORMATION:
            return Label.RELEASE_INFORMATION
        elif item == cls.RELEASE_VERSION:
            return Label.RELEASE_VERSION
        elif item == cls.RELEASE_VERSION_PREFIX:
            return Label.RELEASE_VERSION_PREFIX

        # Video Elements
        elif item == cls.VIDEO_RESOLUTION:
            return Label.VIDEO_RESOLUTION
        elif item in (cls.VIDEO_WIDTH, cls.VIDEO_HEIGHT):
            return Label.VIDEO_RESOLUTION
        elif item == cls.VIDEO_TERM:
            return Label.VIDEO_TERM
        elif item == cls.SOURCE:
            return Label.SOURCE

        # Subtitle Elements
        elif item == cls.SUBS_TERM:
            return Label.SUBS_TERM

        # Delimiters
        elif item == cls.CONTEXT_DELIMITER:
            return Label.CONTEXT_DELIMITER
        elif item == cls.BRACKET:
            return Label.BRACKET
        elif item == cls.DELIMITER:
            return Label.DELIMITER

        # Miscellaneous
        elif item == cls.CONTEXT_DEPENDENT:
            return Label.CONTEXT_DEPENDENT
        elif item == cls.LANGUAGE:
            return Label.LANGUAGE
        elif item == cls.DEVICE_COMPATIBILITY:
            return Label.DEVICE_COMPATIBILITY
        elif item == cls.EXTRA_INFO:
            return Label.EXTRA_INFO

        # Fallback
        return Label.UNKNOWN
