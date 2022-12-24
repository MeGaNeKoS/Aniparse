import json
import logging
from typing import List, Union, Dict, Tuple

import unicodedata

from aniparse.element import ElementCategory
from aniparse.keyword import KeywordOption, Keyword

__all__ = ['KeywordManager']
logger = logging.getLogger(__name__)


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

    def __init__(self):
        self._keys = {}
        self._entries = {}

    @staticmethod
    def normalize(string: str) -> str:
        """
        Normalizes a string by removing accents and converting it to uppercase.

        Args:
        string: The string to normalize.

        Returns:
        The normalized string.
        """
        nfkd = unicodedata.normalize('NFKD', string)
        without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return without_accents.upper()

    def add(self, category: ElementCategory, options: KeywordOption, keywords: List[str]) -> None:
        """
        Add a list of keywords to the keyword manager.
        If a keyword already exists, it will be ignored.
        """
        for keyword in keywords:
            if not keyword:
                continue
            normalized_keyword = self.normalize(keyword)
            if normalized_keyword in self._keys:
                logger.warning(f"Keyword '{keyword}' already exists")
                continue

            self._keys[normalized_keyword] = Keyword(category, options)
            logger.debug('Added keyword: {} with option {}'.format(keyword, options))

    def add_entry(self, category: ElementCategory, keywords: List[str]) -> None:
        """
        Add a new entry to the list of pre-identified keywords.

        Args:
            category: The category of the keywords being added.
            keywords: The list of keywords to add.
        """
        if not isinstance(category, ElementCategory):
            category = ElementCategory(category)

        if category not in self._entries:
            self._entries[category] = set()
        for keyword in keywords:
            normalized_keyword = self.normalize(keyword)
            if normalized_keyword:
                self._entries[category].add(normalized_keyword)

    def find(self, string: str, category: ElementCategory = ElementCategory.UNKNOWN) -> Union[Keyword, None]:
        """
        Search for a keyword in the keyword manager.
        If a keyword is found, it is returned. Otherwise, None is returned.
        """
        logger.debug(f'Searching for keyword: "{string}"')
        keyword = self._keys.get(string, None)
        logger.debug(f'Found keyword: "{keyword}"')
        if (keyword and category != ElementCategory.UNKNOWN
                and keyword.category != category):
            return None
        return keyword

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

            for element_category, kws in keyword_dict.get('keywords', {}).items():
                category = ElementCategory(element_category)
                self.add(category, options, kws)

    def load_entries(self, entries: Union[str, Dict[str, List[str]]]) -> None:
        """
        Load pre-identified keywords from a JSON file or a dictionary.

        Parameters:
        - entries (Union[str, Dict[str, List[str]]]): The file path to the JSON file or a dictionary containing the
          pre-identified keywords for each element category.

        Example:
        ```
        {
            "audio_term": ["Dual Audio", "Multi Audio"],
            "video_term": ["H264", "H.264", "10 bit", "10 bits", "8 bit", "8 bits"],
            "video_resolution": ["480p", "720p", "1080p", "2160p", "4K", "480i", "720i", "1080i"],
            "subtitles": ["Multi Subs", "Multiple Subtitle", "Multiple Subtitles"],
            "source": ["Blu-Ray"]
        }
        ```
        """
        if isinstance(entries, str):
            with open(entries, 'r', encoding="utf-8") as f:
                entries = json.load(f)

        for category, keywords in entries.items():
            self.add_entry(ElementCategory(category), keywords)

    def remove(self, keyword: str) -> Union[Keyword, None]:
        """
        Removes the specified keyword from the keyword manager.

        Parameters:
            keyword (str): The keyword to remove from the keyword manager.

        Returns:
            Keyword: The removed keyword object if the removal was successful.
            None: If the keyword was not found in the keyword manager.
        """
        return self._keys.pop(self.normalize(keyword), None)

    def remove_entries(self, entries: List[Tuple[ElementCategory, List[str]]]) -> None:
        """
        Remove a list of entries from the pre-identified keywords list.

        Args:
            entries: The list of entries to remove. Each entry should be a tuple containing the category
            and a list of keywords.
        """
        for category, keywords in entries:
            for keyword in keywords:
                keyword = self.normalize(keyword)
                if category in self._entries and keyword in self._entries[category]:
                    self._entries[category].remove(keyword)

    def pre_identify_tokens(self, string: str) -> List[Tuple[int, int, ElementCategory]]:
        """
        Identifies and returns all the tokens in the given string that match with the _entries in
        the `self._entries` list.

        Parameters:
        - string (str): The string to search for tokens in.

        Returns:
        - A list of tuple containing the start and end position of the token and the `ElementCategory` it belongs to.
        """
        pre_identified_tokens = []

        for category, keywords in self._entries.items():
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
