import enum


class DescriptorType(enum.Enum):
    """THis category is everything that available during pre-processing"""
    # Series-related elements
    SERIES_TITLE = 'series_title'  # Official title of the series or movie
    SERIES_TYPE = 'series_type'  # Type of series (e.g., TV Show, Anime, Movie)
    SERIES_YEAR = 'series_year'  # Year the series started or movie was released
    SEASON_NUMBER = 'season_number'  # Season of the series, if applicable
    SEASON_PREFIX = 'season_prefix'  # Prefix for the season (e.g., "S", "Season")

    # Episode-related elements
    EPISODE_PREFIX = 'episode_prefix'  # Prefix for the episode (e.g., "E", "Episode")
    EPISODE_NUMBER = 'episode_number'  # Episode number in the series or movie part
    EPISODE_TITLE = 'episode_title'  # Title of the individual episode
    EPISODE_RANGE = 'episode_range'  # Episode range token like "of", "&", "-"
    EPISODE_TOTAL = 'episode_total'  # Total number of episodes in the series
    VOLUME_NUMBER = 'volume_number'  # The volume number in which the episode appears (common for manga)
    VOLUME_PREFIX = 'volume_prefix'  # A prefix to describe the volume (e.g., "Vol.")

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

    def __contains__(self, item: 'DescriptorType') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value

