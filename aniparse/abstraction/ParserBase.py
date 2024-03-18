import logging
from abc import ABC, abstractmethod

from aniparse import WordListManager
from aniparse.token import Tokens

logger = logging.getLogger(__name__)


class PossibilityRule(ABC):
    @classmethod
    @abstractmethod
    def apply(cls, parser: 'AbstractParser'):
        pass


class AbstractParser(ABC):
    tokens: Tokens
    _filename: str
    word_list_manager: WordListManager

    @property
    def filename(self):
        return self._filename
