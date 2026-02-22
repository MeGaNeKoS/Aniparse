from aniparse.core import constant
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag
from aniparse.keyword.AUDIO_TERM import audio_term
from aniparse.keyword.BRACKET import brackets
from aniparse.keyword.CONTENT_TYPE import content_type
from aniparse.keyword.CONTEXT_DELIMITER import context_delimiters
from aniparse.keyword.CONTEXT_DEPENDENT import context_dependent_prefix
from aniparse.keyword.DELIMITER import delimiters
from aniparse.keyword.DEVICE_COMPATIBILITY import device_compatibility_prefix
from aniparse.keyword.EPISODE_PREFIX import episode_prefix
from aniparse.keyword.LANG import language
from aniparse.keyword.RELEASE_INFORMATION import release_information
from aniparse.keyword.RELEASE_VERSION import release_version
from aniparse.keyword.SEASON_PREFIX import season_prefix
from aniparse.keyword.SERIES_TYPE import series_type
from aniparse.keyword.SOURCE import source_prefix
from aniparse.keyword.VOLUME_PREFIX import volume_prefix
from aniparse.keyword.SUBS_TERM import subs_term_prefix
from aniparse.keyword.VIDEO_RESOLUTION import video_resolution
from aniparse.keyword.VIDEO_TERM import video_term_prefix, video_term_suffix

DEFAULT_KEYWORD = [
    *audio_term,
    *context_delimiters,
    *content_type,
    *device_compatibility_prefix,
    *episode_prefix,
    *delimiters,
    *language,
    *release_information,
    *release_version,
    *season_prefix,
    *series_type,
    *source_prefix,
    *subs_term_prefix,
    *video_term_prefix,
    *video_resolution,
    *volume_prefix,
    *video_term_suffix,
    *brackets,
    *context_dependent_prefix,
    ElementEntry(constant.CHECKSUM_PLACEHOLDER, set(), regex_dict={
        r"(?<![a-zA-Z0-9])[a-fA-F0-9]{8}(?![a-zA-Z0-9])": {0: {Tag.FILE_CHECKSUM}}
    }),
    ElementEntry('OF', set(), regex_dict={
        r'(\d+)([\W_])?(OF)([\W_])?(\d+)': {
            1: {Tag.SEQUENCE_NUMBER},
            2: {Tag.CONTEXT_DELIMITER},
            3: {Tag.SEQUENCE_RANGE},
            4: {Tag.CONTEXT_DELIMITER},
            5: {Tag.SEQUENCE_NUMBER}
        }
    })
]
