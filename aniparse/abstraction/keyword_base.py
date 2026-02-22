from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Set, Iterator

import unicodedata

from aniparse.core.token_tags import Tag


@dataclass
class ElementEntry:
    """Represents a single entry in a fuzzy keyword database for filename parsing."""

    word: str
    """The original, non-normalized form of the word. """

    categories: Set[Tag]
    """The set of categories this word can belong to."""

    canonical: str = ""
    """Normalized output form. E.g. 'MOVIES' → canonical='Movie'. If empty, uses word as-is."""

    regex_dict: Dict[str, Dict[int, Set[Tag]]] = field(default_factory=dict)
    """A dictionary of precompiled regex patterns and their associated categories.

    If a word matches a pattern, the corresponding categories are applied.
    """

    def merge(self, other: 'ElementEntry') -> 'bool':
        """Merges two ElementEntry objects if their words are exactly the same.

        :parameter
            other: The other ElementEntry to merge with.

        :return
            True if the entries are merged, and False otherwise.
        """
        if self.word == other.word:
            self.categories.update(other.categories)
            self.regex_dict.update(other.regex_dict)
            return True
        return False


class WordListProvider(ABC):
    """Abstract interface for a provider of word lists for filename parsing."""

    @abstractmethod
    def find(self, normalized_word: str, fuzzy: bool = False, threshold: float = 0.8) -> Iterator[ElementEntry]:
        """Checks if a word exists in the word list, ignoring case.

        Args:
            normalized_word: The normalized form of the word to check (e.g., lowercase, accents removed).

        Returns:
            Return an interator for each element in the word list.
        """
        pass

    @abstractmethod
    def add_word(self, entry: ElementEntry) -> None:
        """Adds a new word entry to the word list.

        Args:
            entry: The ElementEntry object representing the new word.
        """
        pass

    @staticmethod
    def normalize(string: str) -> str:
        """Normalizes a string for consistent comparison.

        This method should be implemented to match the normalization used for storing words.
        """
        nfkd = unicodedata.normalize('NFKD', string)
        without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return without_accents.upper()
