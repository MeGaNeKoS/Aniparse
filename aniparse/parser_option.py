import re

from aniparse import constant


class Options:
    """
    All available options for parsing.
    """
    # Default options, DO NOT CHANGE INTO WEAK REF AS IT USE AS KEY FOR CACHING KEYWORD MANAGER
    _instance = None

    _video_resolution = re.compile(r"\d{3,4}([ip]|([x\u00D7]\d{3,4}))$", flags=re.IGNORECASE)

    def __new__(cls, default=False):
        if default:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        return super().__new__(cls)

    def __init__(self,
                 allowed_delimiter: str = f' _.&+,|',
                 check_title_enclosed: bool = True,
                 context_delimiter: str = f' {constant.DASHES}',
                 delimiter_regex: re.Pattern = None,
                 eps_lower_than_alt: bool = True,
                 ignored_dash: bool = True,
                 ignored_strings: list = None,
                 have_number: re.Pattern = None,
                 keep_delimiters: bool = False,
                 max_extension_length: int = 4,
                 title_before_episode: bool = True,
                 season_part_as_unique: bool = True,
                 video_resolution_pattern: re.Pattern = _video_resolution,
                 *,
                 default=False):
        self.strict = False
        self.allowed_delimiter = allowed_delimiter
        self.check_title_enclosed = check_title_enclosed
        self.context_delimiter = context_delimiter
        self.eps_lower_than_alt = eps_lower_than_alt
        self.ignored_dash = ignored_dash
        self.ignored_strings = ignored_strings or []
        self.keep_delimiters = keep_delimiters
        self.video_resolution_pattern = video_resolution_pattern or re.compile(r".*", flags=re.IGNORECASE)
        self.max_extension_length = max_extension_length
        self.title_before_episode = title_before_episode
        self.season_part_as_unique = season_part_as_unique
        self.min_anime_year = 1900
        self.range_separator = re.compile(rf'([ ~&+{constant.DASHES_PATTERN}])')

        allowed_delimiter += context_delimiter
        if delimiter_regex is None:
            # We want to tokenize by delimiter, but we don't want if it is a number like 5.1, etc
            escaped_delimiters = [re.escape(d) for d in allowed_delimiter]
            if '.' in allowed_delimiter:
                dot_with_digit_before = r'(?<!\d)\.|\.(?!\d)'
                escaped_delimiters.remove(re.escape(''))
                delimiter_pattern = '|'.join(escaped_delimiters + [dot_with_digit_before])
            else:
                delimiter_pattern = '|'.join(escaped_delimiters)

            self.delimiter_regex = re.compile(f"({delimiter_pattern})", flags=re.IGNORECASE)
        else:
            self.delimiter_regex = delimiter_regex

        if have_number is None:
            self.have_number = re.compile(r'\d')

        # Use to restart the keyword manager if the delimiter and context delimiter changed
        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)
