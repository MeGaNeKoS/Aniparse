from collections import defaultdict
from difflib import SequenceMatcher
from typing import Optional, Dict, List, Iterator

from aniparse.abstraction.keyword_base import WordListProvider
from aniparse.keyword import ElementEntry


class InMemoryWordListProvider(WordListProvider):
    """Provides word lists from an in-memory dictionary."""

    def __init__(self):
        """Initializes the provider with an empty dictionary."""
        self.entries: Dict[str, List[ElementEntry]] = defaultdict(list)

    def find(self, normalized_word: str, fuzzy: bool = False, threshold: float = 0.8) -> Iterator[ElementEntry]:
        """Checks if a normalized word exists and return an iterator of it if it does.

        Args:
            normalized_word: The normalized word to check.
            fuzzy: If True, fall back to fuzzy matching when exact match fails.
            threshold: Minimum similarity ratio (0-1) for fuzzy matches.

        Returns:
            An iterator of ElementEntry of the matching normalized word.
        """
        normalized_word = self.normalize(normalized_word)
        if normalized_word in self.entries:
            return iter(self.entries[normalized_word])
        if fuzzy:
            return self._fuzzy_find(normalized_word, threshold)
        return iter([])

    def _fuzzy_find(self, normalized_word: str, threshold: float) -> Iterator[ElementEntry]:
        """Finds entries with keys similar to the given word above the threshold."""
        candidates = []
        for key, entries in self.entries.items():
            ratio = SequenceMatcher(None, normalized_word, key).ratio()
            if ratio >= threshold:
                candidates.append((ratio, entries))
        candidates.sort(key=lambda x: x[0], reverse=True)
        for _, entries in candidates:
            yield from entries

    def add_word(self, entry: ElementEntry) -> None:
        """Adds a new word entry, handling continuations.

        Args:
            entry: The ElementEntry object representing the new word.
        """
        normalized = self.normalize(entry.word)
        self.entries[normalized].append(entry)


class WordListManager:
    """Manages multiple WordListProvider instances and provides a unified interface."""

    def __init__(self):
        """Initializes the manager with an empty list of providers."""
        self._providers: Dict[str, WordListProvider] = {}

    def add_provider(self, name: str, provider: WordListProvider) -> None:
        """Adds a WordListProvider to the manager.

        Args:
            provider: The WordListProvider instance to add.
            name: The name to associate with the provider for later reference
        """
        self._providers[name] = provider

    def get_providers(self) -> List[str]:
        """Returns a list of all registered WordListProviders."""
        return list(self._providers.keys())

    def add_word(self, entry: ElementEntry, provider_name: str) -> None:
        """Adds a new word entry to the specified provider.

        Args:
            entry: The ElementEntry object representing the new word.
            provider_name: The name of the provider to add the word to.
        """
        if provider_name in self._providers:
            self._providers[provider_name].add_word(entry)
        else:
            raise ValueError(f"Provider '{provider_name}' not found.")

    def find(self, normalized_word: str, provider_name: Optional[str] = None, fuzzy: bool = False, threshold: float = 0.8) -> Iterator[ElementEntry]:
        """Checks if a word exists in the specified provider or in all providers.

        Args:
            normalized_word: The normalized form of the word to check.
            provider_name: The name of the provider to check (optional). If None, all providers are checked.

        Yields:
            ElementEntry objects from the specified provider (or all providers) that contain the word.
        """
        if provider_name:
            if provider_name in self._providers:
                yield from self._providers[provider_name].find(normalized_word, fuzzy=fuzzy, threshold=threshold)
            else:
                raise ValueError(f"Provider '{provider_name}' not found.")
        else:
            for provider in self._providers.values():
                yield from provider.find(normalized_word, fuzzy=fuzzy, threshold=threshold)

