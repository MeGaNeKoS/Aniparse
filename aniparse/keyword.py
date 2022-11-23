import logging
from typing import List, Union

import unicodedata

from aniparse.element import ElementCategory

__all__ = ['option', 'KeywordManager', 'BaseKeywordManager']

logger = logging.getLogger(__name__)


class KeywordOption:
    def __init__(self, identifiable=True, searchable=True, valid=True):
        self.identifiable = identifiable
        self.searchable = searchable
        self.valid = valid


class Keyword:
    def __init__(self, e_category: ElementCategory, options: KeywordOption):
        self.e_category = e_category
        self.options = options


option = {
    "default": KeywordOption(),
    "invalid": KeywordOption(valid=False),
    "unidentifiable": KeywordOption(identifiable=False),
    "unidentifiable_invalid": KeywordOption(identifiable=False, valid=False),
    "unidentifiable_unsearchable": KeywordOption(identifiable=False, searchable=False)

}


class BaseKeywordManager:
    def __init__(self):
        self._file_extensions = {}
        self._keys = {}

    def _get_keyword_container(self, category) -> dict:
        """
        File extensions are stored in a separate container
        """
        return self._file_extensions if category == ElementCategory.FILE_EXTENSION else self._keys

    def add(self, category: ElementCategory, options: KeywordOption, keywords: List[str]) -> None:
        keyword_container = self._get_keyword_container(category)
        for keyword in keywords:
            if not keyword:
                continue
            if keyword in keyword_container:
                continue

            keyword_container[keyword] = Keyword(category, options)
            logger.debug('Added keyword: {} with option {}'.format(keyword, options))

    def find(self, string: str, e_category: ElementCategory = ElementCategory.UNKNOWN) -> Union[Keyword, None]:
        """
        Find a keyword in the string based on the category

        :param string:
        :param e_category:
        :return:
        """
        logger.debug('Searching for keyword: {}'.format(string))
        keyword_container = self._get_keyword_container(e_category)
        if string not in keyword_container:
            return None
        keyword = keyword_container[string]
        if (e_category != ElementCategory.UNKNOWN
                and keyword.e_category != e_category):
            return None
        return keyword

    @staticmethod
    def normalize(string: str) -> str:
        """
        Remove accents and other special symbols
        NFKD: Normalization Form Compatibility Decomposition, (Normalize form with change the length)
        """
        nfkd = unicodedata.normalize('NFKD', string)
        without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return without_accents.upper()

    @staticmethod
    def peek(string: str) -> list:
        """
        this to handle the case where the string are seperated by a delimiter (space)
        e.g. "H264-Flac" -> ["H264", "Flac"]
        this early peek have many things to improve, but for now it's good enough
        """
        entries = [
            (ElementCategory.AUDIO_TERM, ['Dual Audio', 'Multi Audio']),
            (ElementCategory.VIDEO_TERM, ['H264', 'H.264', "10 bit", "10 bits", "8 bit", "8 bits"]),
            (ElementCategory.VIDEO_RESOLUTION, ['480p', '720p', '1080p', '2160p', '4K', "480i", "720i", "1080i"]),
            (ElementCategory.SUBTITLES, ['Multi Subs', 'Multiple Subtitle', 'Multiple Subtitles']),
            (ElementCategory.SOURCE, ['Blu-Ray'])
        ]

        pre_identified_tokens = []

        for category, keywords in entries:
            for keyword in keywords:
                keyword_begin_pos = string.lower().find(keyword.lower())
                if keyword_begin_pos != -1:  # Found the keyword in the string
                    keyword_end_pos = keyword_begin_pos + len(keyword)
                    pre_identified_tokens.append(
                        (keyword_begin_pos, keyword_end_pos, category))
        pre_identified_tokens = sorted(pre_identified_tokens,
                                       key=lambda x: (x[0], -x[1]))  # lowest begin pos, the highest end pos
        # check for overlapping tokens
        # e.g. (0, 3, "Sub") and (0, 4, "Subs")
        # if the first token is a substring of the second token, remove the first token
        last_token = (-1, -1, None)
        for token in pre_identified_tokens.copy():
            if token[0] == last_token[0]:
                pre_identified_tokens.remove(token)
            last_token = token

        return sorted(pre_identified_tokens)


class KeywordManager(BaseKeywordManager):
    """
    Default Keyword Manager
    """
    def __init__(self):
        super().__init__()

        self.add(ElementCategory.ANIME_SEASON_PREFIX, option["default"], [
            'SAISON', 'SEASON'
        ])

        self.add(ElementCategory.ANIME_SEASON_PREFIX, option["unidentifiable"], [
            'S'])

        self.add(ElementCategory.ANIME_TYPE, option["unidentifiable_unsearchable"], [
            'GEKIJOUBAN', 'MOVIE',
            'OAD', 'OAV', 'ONA', 'OVA',
            'SPECIAL', 'SPECIALS',
            'TV'
        ])

        self.add(ElementCategory.ANIME_TYPE,
                 option["unidentifiable_unsearchable"],
                 ['SP'])  # e.g. "Yumeiro Patissiere SP Professional"

        self.add(ElementCategory.ANIME_TYPE, option["unidentifiable_invalid"], [
            'ED', 'ENDING', 'NCED', "CLEAN ENDING",
            'NCOP', 'OP', 'OPENING', "CLEAN OPENING",
            'PREVIEW', 'PV'
        ])

        self.add(ElementCategory.AUDIO_TERM, option["default"], [
            # Audio channels
            '2.0CH', '2CH', '5.1', '5.1CH', 'DTS', 'DTS-ES', 'DTS5.1',
            'TRUEHD5.1',
            # Audio codec
            'AAC', 'AACX2', 'AACX3', 'AACX4', 'AC3', 'EAC3', 'E-AC-3',
            'FLAC', 'FLACX2', 'FLACX3', 'FLACX4', 'LOSSLESS', 'MP3', 'OGG',
            'VORBIS',
            # Audio language
            'DUALAUDIO', 'DUAL AUDIO', 'DUAL-AUDIO',
            'MULTIAUDIO', 'MULTI AUDIO', 'MULTI-AUDIO'
        ])

        self.add(ElementCategory.DEVICE_COMPATIBILITY, option["default"], [
            'IPAD3', 'IPHONE5', 'IPOD', 'PS3', 'XBOX', 'XBOX360'
        ])

        self.add(ElementCategory.DEVICE_COMPATIBILITY, option["unidentifiable"], [
            'ANDROID'
        ])

        self.add(ElementCategory.EPISODE_PREFIX, option["default"], [
            'EP', 'EP.', 'EPS', 'EPS.', 'EPISODE', 'EPISODE.', 'EPISODES',
            'CAPITULO', 'EPISODIO', 'FOLGE'
        ])

        self.add(ElementCategory.EPISODE_PREFIX, option["invalid"], [
            'E'
        ])  # single-letter episode keywords are not valid

        self.add(ElementCategory.FILE_EXTENSION, option["default"], [
            '3GP', 'AVI', 'DIVX', 'FLV', 'M2TS', 'MKV', 'MOV', 'MP4', 'MPG',
            'OGM', 'RM', 'RMVB', 'TS', 'WEBM', 'WMV'
        ])

        self.add(ElementCategory.FILE_EXTENSION, option["invalid"], [
            'AAC', 'AIFF', 'FLAC', 'M4A', 'MP3', 'MKA', 'OGG', 'WAV', 'WMA',
            '7Z', 'RAR', 'ZIP',
            'ASS', 'SRT'
        ])

        self.add(ElementCategory.LANGUAGE, option["default"], [
            'ENG', 'ENGLISH', 'ESPANOL', 'JAP', 'PT-BR', 'SPANISH', 'VOSTFR'
        ])

        self.add(ElementCategory.LANGUAGE, option["unidentifiable"], [
            'ESP', 'ITA'
        ])  # e.g. "Tokyo ESP", "Bokura ga Ita"

        self.add(ElementCategory.OTHER, option["default"], [
            'REMASTER', 'REMASTERED', 'UNCENSORED', 'UNCUT',
            'TS', 'VFR', 'WIDESCREEN', 'WS'
        ])

        self.add(ElementCategory.RELEASE_INFORMATION, option["default"], [
            'BATCH', 'COMPLETE', 'PATCH', 'REMUX'
        ])

        self.add(ElementCategory.RELEASE_INFORMATION, option["unidentifiable"], [
            'END', 'FINAL'
        ])  # e.g. "The End of Evangelion", "Final Approach"

        self.add(ElementCategory.RELEASE_VERSION, option["default"], [
            'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10'
        ])

        self.add(ElementCategory.SOURCE, option["default"], [
            'BD', 'BDRIP', 'BLURAY', 'BLU-RAY',
            'DVD', 'DVD5', 'DVD9', 'DVD-R2J', 'DVDRIP', 'DVD-RIP',
            'R2DVD', 'R2J', 'R2JDVD', 'R2JDVDRIP',
            'HDTV', 'HDTVRIP', 'TVRIP', 'TV-RIP',
            'WEBCAST', 'WEBRIP'
        ])

        self.add(ElementCategory.SUBTITLES, option["default"], [
            'ASS', 'BIG5', 'DUB', 'DUBBED', 'HARDSUB', 'HARDSUBS', 'RAW',
            'SOFTSUB', 'SOFTSUBS', 'SUB', 'SUBBED', 'SUBTITLED',
            'MULTI SUBS', 'MULTI-SUBS', 'MULTISUB', 'MULTISUBS'
        ])

        self.add(ElementCategory.VIDEO_TERM, option["default"], [
            # Frame rate
            '23.976FPS', '24FPS', '29.97FPS', '30FPS', '60FPS', '120FPS',
            # Video codec
            '8BIT', '8-BIT', '10BIT', '10BITS', '10-BIT', '10-BITS',
            'HI10', 'HI10P', 'HI444', 'HI444P', 'HI444PP',
            'H264', 'H265', 'H.264', 'H.265', 'X264', 'X265', 'X.264',
            'AVC', 'HEVC', 'HEVC2', 'DIVX', 'DIVX5', 'DIVX6', 'XVID',
            # Video format
            'AVI', 'RMVB', 'WMV', 'WMV3', 'WMV9',
            # Video quality
            'HQ', 'LQ',
            # Video resolution
            'HD', 'SD'
        ])

        self.add(ElementCategory.VOLUME_PREFIX, option["default"], [
            'VOL', 'VOL.', 'VOLUME'
        ])
