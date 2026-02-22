from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type

from aniparse.config import ParserConfig
from aniparse.wordlist import WordListManager
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token import Tokens, Token

if TYPE_CHECKING:
    from aniparse.core.rhythm import DelimiterProfile

logger = logging.getLogger(__name__)


class AbstractParser(ABC):
    tokens: Tokens
    _filename: str
    word_list_manager: WordListManager
    delimiter_profile: DelimiterProfile
    config: ParserConfig

    @property
    def filename(self):
        return self._filename

    @abstractmethod
    def process_entry(self, word: str, tokens: list[Token], entry: ElementEntry):
        pass


class PossibilityRule(ABC):
    @classmethod
    @abstractmethod
    def apply(cls, parser: AbstractParser):
        pass


class Possibilities:
    """Ordered collection of possibility rules."""

    def __init__(self):
        self._rules: list[Type[PossibilityRule]] = []

    def add_rule(self, rule: Type[PossibilityRule]):
        self._rules.append(rule)

    def apply_all(self, parser: AbstractParser):
        for rule in self._rules:
            rule.apply(parser)
