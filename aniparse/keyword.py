import json
import logging
import re
import unicodedata
import weakref
from typing import Dict, Tuple, List, Union

from aniparse.parser_option import Options
from aniparse.element import ElementCategory

__all__ = ['KeywordOption', 'Keyword', 'KeywordManager']

from aniparse.token import Token, Tokens

logger = logging.getLogger(__name__)

DEFAULT_KEYWORD = [
    {
        'identifiable': True,
        'searchable': True,
        'valid': True,
        'keywords': {
            'anime_season_prefix.txt': ['SAISON', 'SEASON'],
            'audio_term': [
                '2.0CH', '2CH', '5.1', '5.1CH', 'DTS', 'DTS-ES', 'DTS5.1',
                'TRUEHD5.1', 'AAC', 'AACX2', 'AACX3', 'AACX4', 'AC3', 'EAC3',
                'E-AC-3', 'FLAC', 'FLACX2', 'FLACX3', 'FLACX4', 'LOSSLESS', 'MP3',
                'OGG', 'VORBIS', 'DUALAUDIO', 'DUAL AUDIO', 'DUAL-AUDIO',
                'MULTIAUDIO', 'MULTI AUDIO', 'MULTI-AUDIO'
            ],
            'device_compatibility': ['IPAD3', 'IPHONE5', 'IPOD', 'PS3', 'XBOX', 'XBOX360'],
            'episode_prefix': ['EP', 'EP.', 'EPS', 'EPS.', 'EPISODE', 'EPISODE.', 'EPISODES',
                               'CAPITULO', 'EPISODIO', 'FOLGE'],
            'language': ['ENG', 'ENGLISH', 'ESPANOL', 'JAP', 'PT-BR', 'SPANISH', 'VOSTFR'],
            'other': ['REMASTER', 'REMASTERED', 'UNCENSORED', 'UNCUT', 'TS', 'VFR',
                      'WIDESCREEN', 'WS'],
            'release_information': ['BATCH', 'COMPLETE', 'PATCH', 'REMUX'],
            'release_version': ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
                                'V10'],
            'source': ['BD', 'BDRIP', 'BLURAY', 'BLU-RAY', 'DVD', 'DVD5', 'DVD9', 'DVD-R2J',
                       'DVDRIP', 'DVD-RIP', 'R2DVD', 'R2J', 'R2JDVD', 'R2JDVDRIP', 'HDTV',
                       'HDTVRIP', 'TVRIP', 'TV-RIP', 'WEBCAST', 'WEBRIP'],
            'subtitles': ['ASS', 'BIG5', 'DUB', 'DUBBED', 'HARDSUB', 'HARDSUBS', 'RAW',
                          'SOFTSUB', 'SOFTSUBS', 'SUB', 'SUBBED', 'SUBTITLED', 'MULTI SUBS',
                          'MULTI-SUBS', 'MULTISUB', 'MULTISUBS', "Multiple Subtitle",
                          "Multiple Subtitles"],
            "video_resolution": ["480p", "720p", "1080p", "2160p", "4K", "480i", "720i", "1080i"],
            'video_term': ['23.976FPS', '24FPS', '29.97FPS', '30FPS', '60FPS', '120FPS',
                           '8BIT', "8 BITS", '8-BIT', '10BIT', '10BITS', "10 BIT", "10 BITS",
                           '10-BIT', '10-BITS', 'HI10', 'HI10P', 'HI444', 'HI444P', 'HI444PP', 'H264', 'H265',
                           'H.264', 'H.265', 'X264', 'X265', 'X.264', 'AVC', 'HEVC', 'HEVC2', 'DIVX', 'DIVX5',
                           'DIVX6', 'XVID', 'AVI', 'RMVB', 'WMV', 'WMV3', 'WMV9', 'HQ', 'LQ', 'HD', 'SD'],
            'volume_prefix': ['VOL', 'VOL.', 'VOLUME']
        }
    },
    {
        'identifiable': False,
        'searchable': True,
        'valid': True,
        'keywords': {
            'anime_season_prefix.txt': ['S'],
            'device_compatibility': ['ANDROID'],
            'language': ['ESP', 'ITA'],
        }
    },
    {
        'identifiable': False,
        'searchable': True,
        'valid': True,
        'keywords': {
            'release_information': ['END', 'FINAL']
        },
        'invalid_prefix': ['THE']
    },
    {
        'identifiable': False,
        'searchable': False,
        'valid': True,
        'keywords': {
            'anime_type': ['GEKIJOUBAN', 'MOVIE', 'OAD', 'OAV', 'ONA', 'OVA', 'SPECIAL', 'SPECIALS',
                           'TV', 'SP']}
    }, {
        'identifiable': False,
        'searchable': True
        , 'valid': False,
        'keywords': {
            'anime_type': ['ED', 'ENDING', 'NCED', 'CLEAN ENDING',
                           'NCOP', 'OP', 'OPENING', 'CLEAN OPENING',
                           'PREVIEW', 'PV']}},
    {
        'identifiable': True,
        'searchable': True,
        'valid': False,
        'keywords': {
            'episode_prefix': ['E'],

        }
    }
]


class KeywordOption:
    """
    A class representing the options for a `Keyword`.

    The options for a `Keyword` include whether it is identifiable, searchable, and valid.

    Properties:
        identifiable: A boolean indicating whether the `Keyword` can be identified.
        searchable: A boolean indicating whether the `Keyword` can be searched for.
        valid: A boolean indicating whether the `Keyword` is valid.
    """

    _instances: Dict[Tuple[bool, bool, bool], 'KeywordOption'] = weakref.WeakValueDictionary()

    def __new__(cls, identifiable: bool = True, searchable: bool = True, valid: bool = True):
        """
        Create a new instance of `KeywordOption` if it doesn't already exist.
        Otherwise, return the existing instance.
        """
        key = (identifiable, searchable, valid)
        if key in cls._instances:
            return cls._instances[key]

        instance = super().__new__(cls)
        cls._instances[key] = instance
        return instance

    def __init__(self, identifiable: bool = True, searchable: bool = True, valid: bool = True):
        """
        Initialize a `KeywordOption` instance with the given options.
        """
        self.__identifiable = identifiable
        self.__searchable = searchable
        self.__valid = valid

    @property
    def identifiable(self) -> bool:
        """
        A boolean indicating whether the `Keyword` can be identified.
        """
        return self.__identifiable

    @property
    def searchable(self) -> bool:
        """
        A boolean indicating whether the `Keyword` can be searched for.
        """
        return self.__searchable

    @property
    def valid(self) -> bool:
        """
        A boolean indicating whether the `Keyword` is valid.
        """
        return self.__valid


class Keyword:
    """
    A class representing a keyword in an anime filename.

    A keyword is an element in the filename that has a specific category (e.g. ANIME_SEASON, ANIME_TYPE, etc.)
    and a set of options (e.g. case sensitivity, searchable, etc.)
    that can be used to customize the parsing and search behavior of the element.

    Attributes:
    category (ElementCategory): The element category of the keyword (e.g. ANIME_SEASON, ANIME_TYPE, etc.)
    """
    _instances: Dict[Tuple[ElementCategory, KeywordOption], 'Keyword'] = weakref.WeakValueDictionary()

    def __new__(cls, category: ElementCategory, options: KeywordOption):
        """
        Create a new instance of `KeywordOption` if it doesn't already exist.
        Otherwise, return the existing instance.
        """
        key = (category, options)
        if key in cls._instances:
            return cls._instances[key]

        instance = super().__new__(cls)
        cls._instances[key] = instance
        return instance

    def __init__(self, category: ElementCategory, options: KeywordOption = KeywordOption(),
                 invalid_prefix: List[str] = None):
        self.invalid_prefix = invalid_prefix or []
        self.__category = category
        self.__options = options

    @property
    def category(self) -> ElementCategory:
        """
        The element category of the keyword (e.g. ANIME_SEASON, ANIME_TYPE, etc.)
        """
        return self.__category

    @property
    def options(self) -> KeywordOption:
        """
        The options for the keyword.
        """
        return self.__options


class KeywordManager:
    """
    Manages a list of keywords and their options.

    Keywords are stored in a dictionary where the keys are the normalized
    versions of the keywords (converted to uppercase and with accents removed).
    The values are `Keyword` objects containing the category and options for the
    keyword.

    Keywords can be added to the manager using the `add` method and retrieved
    using the `find` method.
    """

    _instances: Dict[Options, 'KeywordManager'] = weakref.WeakValueDictionary()
    # aacx3, flacx5 -> aac, flac and so on
    # Only valid for ElementCategory.AUDIO_TERM
    # TODO: add support from parser_options instead of hard coding
    keyword_multiplier_pattern = re.compile(r"^(.*?)(?=x\d+$|$)", flags=re.IGNORECASE)

    def __new__(cls, options: Options, keywords: Dict[ElementCategory, List[str]] = None, *, cache: bool = False):
        """
        Create a new instance of `KeywordOption` if it doesn't already exist.
        Otherwise, return the existing instance.
        """

        if cache:
            if options in cls._instances:
                return cls._instances[options]

        instance = super().__new__(cls)

        if cache:
            cls._instances[options] = instance
        return instance

    def __init__(self, options: Options, keywords: Dict[ElementCategory, List[str]] = None, *, cache: bool = False):
        self._keys = {}
        self._delimited_key = {}
        self.options = options
        # TODO: Still in IDEA
        options.add_observer(self)

        self.load_keywords(keywords or DEFAULT_KEYWORD)

    @staticmethod
    def normalize(string: str) -> str:
        """
        Normalizes a string by removing accents and converting it to uppercase.

        Parameter:
            string (str): The string to normalize.

        Return:
            The normalized string.
        """
        nfkd = unicodedata.normalize('NFKD', string)
        without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return without_accents.upper()

    def add(self,
            category: ElementCategory,
            options: KeywordOption,
            keywords: List[str],
            invalid_prefix: List[str] = None) -> None:
        """
        Add a list of keywords to the keyword manager.
        If a keyword already exists, it will be ignored.

        Parameters:
            category (ElementCategory): The category of the keywords.
            options (KeywordOption): The options for the keywords.
            keywords (List[str]): The list of keywords to add.
            invalid_prefix (List[str]): The list of invalid prefixes for the keywords.

        Return:
            None
        """
        for keyword in keywords:
            if not keyword:
                continue

            normalized_keyword = self.normalize(keyword)
            # TODO: add support from parser_options instead of hard coding
            #  We dont need this if we make sure the keyword doesnt have a multiplier for this part
            if category == ElementCategory.AUDIO_TERM:
                normalized_keyword = self.keyword_multiplier_pattern.match(normalized_keyword).group(1)

            delimited_keyword = [key for key in self.options.delimiter_regex.split(normalized_keyword) if key]

            if normalized_keyword in self._keys:
                logger.warning(f"Keyword '{delimited_keyword}' already exists")
                continue

            # The keyword contains a delimiter
            if len(delimited_keyword) > 1:
                if not delimited_keyword[0] in self._delimited_key:
                    self._delimited_key[delimited_keyword[0]] = set()

                substring = ""
                for sub_key in delimited_keyword:
                    substring += sub_key
                    self._delimited_key[delimited_keyword[0]].add(substring)

            self._keys[normalized_keyword] = Keyword(category, options, invalid_prefix)
            logger.debug(f'Added keyword: {keyword} with options: {options}')

    def in_delimited_keywords(self, word: str) -> bool:
        string = self.keyword_multiplier_pattern.match(self.normalize(word)).group(1)
        return string in self._delimited_key

    def find(self, token: Token) -> Keyword:
        string = self.keyword_multiplier_pattern.match(self.normalize(token.content)).group(1)
        return self._keys.get(string) or self._keys.get(token.content)

    def find_all(self, tokens: Tokens, token: Token) -> Tuple[Union[Keyword, None], Token]:
        """
            Search for a keyword in the keyword manager.
            If a keyword is found, it is returned. Otherwise, None is returned.

            Parameter:
                token (Token): The token to search for.

            Return:
                A tuple containing the keyword and the last token it checks.
        """

        string = self.keyword_multiplier_pattern.match(self.normalize(token.content)).group(1)

        logger.debug(f'Searching for keyword: "{string}"')
        delimited_keyword = self._delimited_key.get(string, None)
        if delimited_keyword:
            logger.debug(f"Found in delimited keyword: '{string}'")
            logger.debug(f"Attempting to find full keyword")
            full_keyword = ""
            key = token
            for key in tokens.loop_forward(begin=token):
                if full_keyword + self.normalize(key.content) not in delimited_keyword:
                    break
                full_keyword += self.normalize(key.content)
            keyword = self._keys.get(full_keyword, None)
            if keyword:
                if string != self.normalize(token.content):
                    # TODO: add support from parser_options instead of hard coding
                    if keyword is not ElementCategory.AUDIO_TERM:
                        return None, token
                logger.debug(f'Found full keyword: "{full_keyword}"')
            return keyword, key

        return self._keys.get(string) or self._keys.get(token.content), token

    def load_keywords(self, keywords: Union[str, List[Dict[str, Union[bool, Dict[str, List]]]]]) -> None:
        """
        Load keywords from a JSON file or a list of dictionaries.

        Parameters:
        - keywords (Union[str, List[Dict[str, Union[bool, Dict[str, List]]]]]): The file path to the JSON file
          or a list of dictionaries containing the keyword options and keywords for each element category.

        Example:
        ```
        [
            {
              "identifiable": true,
              "searchable": true,
              "valid": true,
              "keywords": {
                "audio_term": ["AAC", "MP3"]
              }
            },
            {
              "identifiable": true,
              "searchable": false,
              "valid": true,
              "keywords": {
                "video_term": ["H.264", "H.265"]
              }
            }
        ]
        ```
        """
        if isinstance(keywords, str):
            with open(keywords, 'r', encoding="utf-8") as f:
                keywords = json.load(f)

        self._keys.clear()
        for keyword_dict in keywords:
            is_identifiable = keyword_dict.get('identifiable', True)
            is_searchable = keyword_dict.get('searchable', True)
            is_valid = keyword_dict.get('valid', True)
            options = KeywordOption(is_identifiable, is_searchable, is_valid)
            invalid_prefix = keyword_dict.get('invalid_prefix', None)

            for element_category, keywords_ in keyword_dict.get('keywords', {}).items():
                try:
                    category = ElementCategory(element_category)
                except ValueError:
                    logger.warning(f"Invalid element category: {element_category}")
                    continue
                self.add(category, options, keywords_, invalid_prefix)

    def get_episode_prefix(self, word):
        prefix = []
        for index, _ in enumerate(word):
            if self._keys.get(self.normalize(word[:index + 1])):
                prefix.append(word[:index + 1])
        return prefix[-1] if prefix else None
