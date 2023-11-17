from aniparse import constant
from aniparse.element import DescriptorType
from aniparse.keyword.AUDIO_TERM import audio_term_prefix, audio_term_suffix
from aniparse.keyword.BRACKET import bracket_prefix
from aniparse.keyword.CONTEXT_DELIMITER import context_delimiters
from aniparse.keyword.CONTEXT_DEPENDENT import context_dependent_prefix
from aniparse.keyword.DELIMITER import delimiters
from aniparse.keyword.DEVICE_COMPATIBILITY import device_compatibility_prefix
from aniparse.keyword.EPISODE_PREFIX import episode_prefix
from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.keyword.LANG import language_prefix
from aniparse.keyword.OTHER import other_prefix
from aniparse.keyword.RELEASE_INFORMATION import release_information_prefix
from aniparse.keyword.RELEASE_VERSION import release_version_prefix
from aniparse.keyword.SEASON_PREFIX import season_prefix
from aniparse.keyword.SERIES_TYPE import series_type_prefix
from aniparse.keyword.SOURCE import source_prefix
from aniparse.keyword.SUBS_TERM import subs_term_prefix
from aniparse.keyword.VIDEO_RESOLUTION import video_resolution_suffix, video_resolution_infix
from aniparse.keyword.VIDEO_TERM import video_term_prefix, video_term_suffix


DEFAULT_PREFIX_KEYWORD = [
    *audio_term_prefix,
    *context_delimiters,
    *device_compatibility_prefix,
    *episode_prefix,
    *delimiters,
    *language_prefix,
    *other_prefix,
    *release_information_prefix,
    *release_version_prefix,
    *season_prefix,
    *series_type_prefix,
    *source_prefix,
    *subs_term_prefix,
    *video_term_prefix
]

DEFAULT_SUFFIX_KEYWORD = [
    *audio_term_suffix,
    *video_resolution_suffix,
    *video_term_suffix
]

DEFAULT_SPECIAL_KEYWORD = [
    *bracket_prefix,
    *context_dependent_prefix,
    *video_resolution_infix,
    ElementEntry(constant.CHECKSUM_PLACEHOLDER, set(), regex_dict={
        r"\b[a-fA-F0-9]{8}": {0: {DescriptorType.FILE_CHECKSUM}}
    }),
    ElementEntry('OF', set(), regex_dict={
        r'(\d+)([\W_])?(OF)([\W_])?(\d+)': {
            1: {DescriptorType.EPISODE_NUMBER},
            2: {DescriptorType.CONTEXT_DELIMITER},
            3: {DescriptorType.EPISODE_RANGE},
            4: {DescriptorType.CONTEXT_DELIMITER},
            5: {DescriptorType.EPISODE_TOTAL}
        }
    })
]
