import enum
import re

from typing import Optional, Dict, Union, List, Iterator

import unicodedata

from aniparse.keyword import ElementEntry


class Table(enum.Enum):
    PREFIX = 'prefix'
    SUFFIX = 'suffix'
    INFIX = 'infix'


class WordListProvider:
    def exists(self, token: str, table: Table = None) -> Iterator[ElementEntry]:
        """Check if a substring exists within a category. If no category is provided, search across all."""
        raise NotImplementedError

    def add_word(self, entry: ElementEntry, table: Table = Table.PREFIX):
        """Add new word to the database"""
        raise NotImplementedError

    @staticmethod
    def normalize(string: str) -> str:
        nfkd = unicodedata.normalize('NFKD', string)
        without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return without_accents.upper()


class InMemoryWordListProvider(WordListProvider):
    def __init__(self):
        self.prefix: Dict[str, ElementEntry] = {}
        self.suffix: Dict[str, ElementEntry] = {}
        self.special: Dict[str, ElementEntry] = {}

    def add_word(self, entry: ElementEntry, table: Table = Table.PREFIX):
        word = self.normalize(entry.word)
        if table == Table.PREFIX:
            target_dict = self.prefix
        elif table == Table.SUFFIX:
            target_dict = self.suffix
        elif table == Table.INFIX:
            target_dict = self.special
        else:
            raise ValueError('Invalid table type')

        # Extract the first group of alphabetic characters from the original word
        match = re.search(r'[A-Z]+(.*)', word)
        if match and match.group(1):
            continuation_word = match.group(1)
            new_entry = ElementEntry(continuation_word, set(), continuation_set={word})

            if continuation_word in target_dict:
                target_dict[continuation_word].merge(new_entry)
            else:
                target_dict[continuation_word] = new_entry

        if word in target_dict:
            target_dict[word].merge(entry)
        else:
            target_dict[word] = entry

    def exists(self, token: str, table: Table = None) -> Iterator[ElementEntry]:
        normalized_token = self.normalize(token)

        if table == Table.PREFIX or table is None:
            entry = self.prefix.get(normalized_token, None)
            if entry is not None:
                yield entry

        if table == Table.SUFFIX or table is None:
            entry = self.suffix.get(normalized_token, None)
            if entry is not None:
                yield entry

        if table == Table.INFIX or table is None:
            entry = self.special.get(normalized_token, None)
            if entry is not None:
                yield entry


class WordListManager:
    def __init__(self):
        self.providers: List[WordListProvider] = []

    def add_provider(self, provider: WordListProvider):
        self.providers.append(provider)

    def add_word(self, entry: ElementEntry, table: Table = Table.PREFIX):
        for provider in self.providers:
            provider.add_word(entry, table)

    def exists(self, token: str, table: Table = None) -> Iterator[ElementEntry]:
        for provider in self.providers:
            results = provider.exists(token, table)
            for result in results:
                yield result
