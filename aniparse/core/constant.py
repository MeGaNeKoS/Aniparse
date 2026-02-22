"""Structural constants for the aniparse pipeline (fixed, internal)."""
from aniparse.core.token_tags import Tag

OPEN_BRACKETS = (
    "(",  # U+0028 LEFT PARENTHESIS
    "[",  # U+005B LEFT SQUARE BRACKET
    "{",  # U+007B LEFT CURLY BRACKET
    "\u300C",  # Corner bracket
    "\u300E",  # White corner bracket
    "\u3010",  # Black lenticular bracket
    "\uFF08",  # Fullwidth parenthesis
)

CLOSE_BRACKETS = (
    ")",  # U+0029 Right parenthesis
    "]",  # U+005D Right square bracket
    "}",  # U+007D Right curly bracket
    "\u300D",  # Corner bracket
    "\u300F",  # White corner bracket
    "\u3011",  # Black lenticular bracket
    "\uFF09",  # Fullwidth right parenthesis
)

BRACKETS = OPEN_BRACKETS + CLOSE_BRACKETS

# Parenthesis-style brackets (used for titles/alternatives, not metadata)
OPEN_PARENS = ("(", "\uFF08")  # ASCII + Fullwidth parenthesis

# Map open bracket to its matching close bracket (same index)
BRACKET_PAIRS = dict(zip(OPEN_BRACKETS, CLOSE_BRACKETS))

DASHES = "-\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uFE58\uFE63\uFF0D"
UNDERSCORE = "_"  # Universal space substitute in filenames
DELIMITERS = f".{UNDERSCORE}+, {DASHES}"
CONTEXT_DELIMITER = DASHES

SPACE = " "  # Output space (replaces underscores/delimiters in titles)
APOSTROPHE = "'"  # Possessive marker (e.g., "queen's")
DOT = "."  # Decimal separator in titles (e.g., "3.33")
COMMA = ","  # List separator

# Video resolution suffixes (e.g., 1080p, 720i, 4k)
VIDEO_RESOLUTION_SUFFIXES = frozenset({"p", "i"})
VIDEO_RESOLUTION_MULTIPLIER_SUFFIXES = frozenset({"k"})

PIPE = "|"  # Series alternative separator

CHECKSUM_PLACEHOLDER = "<CHECKSUM>"
DEFAULT_PROVIDER_NAME = "InMemory"

# Structural zone constants
ZONE_TITLE = "title"
ZONE_TRANSITION = "transition"
ZONE_METADATA = "metadata"

# Label sets — shared base for rules that need to classify "metadata" tokens.
# Individual rules extend this with context-specific labels.
BASE_METADATA_LABELS = frozenset({
    Tag.VIDEO_RESOLUTION, Tag.SOURCE,
    Tag.AUDIO_TERM, Tag.VIDEO_TERM,
    Tag.FILE_CHECKSUM, Tag.SUBS_TERM,
    Tag.LANGUAGE, Tag.DEVICE_COMPATIBILITY,
    Tag.RELEASE_VERSION, Tag.RELEASE_INFORMATION,
})

# Common metadata indicator words (for heuristic checks, e.g., pipe-split cleanup)
BASE_METADATA_INDICATORS = frozenset({
    'bd', 'dvd', 'remux', '1080p', '720p', 'x264', 'x265',
    'flac', 'aac', 'hevc', 'dual',
})

# Common video resolutions (bare numbers without 'p' suffix)
COMMON_RESOLUTIONS = frozenset({360, 480, 576, 720, 1080, 1440, 2160, 4320})

# Known media file extensions
FILE_EXTENSIONS = frozenset({
    "3gp", "avi", "divx", "flv", "m2ts", "m4v", "mkv", "mov", "mp4", "mpg",
    "mpeg", "ogm", "ogv", "rmvb", "ts", "webm", "wmv",
    "aac", "ac3", "dts", "flac", "mp3", "ogg", "wav", "wma",
    "ass", "srt", "ssa", "sub", "sup", "idx",
    "7z", "rar", "zip", "gz",
})

