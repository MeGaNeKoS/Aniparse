import logging
from dataclasses import dataclass, field
from typing import Set, Dict, Union

from aniparse.element import Label, Metadata

logger = logging.getLogger(__name__)


@dataclass
class ElementEntry:
    word: str
    category_set: Set[Union[Label, Metadata]]
    regex_dict: Dict[str, Dict[int, Set[Union[Label, Metadata]]]] = field(default_factory=dict)
    continuation_set: Set[str] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return isinstance(other, ElementEntry) and self.word == other.word

    def merge(self, other_entry):
        if not self.word or not other_entry.word:
            logger.error("Cannot merge ElementEntries with empty words")
            return

        # Merge category sets
        self.category_set.update(other_entry.category_set)

        # Merge continuation dictionaries
        self.continuation_set.update(other_entry.continuation_set)

        # Merge regex dictionaries
        for k, v in other_entry.regex_dict.items():
            if k in self.regex_dict:
                self.regex_dict[k].update(v)
            else:
                self.regex_dict[k] = v.copy()
