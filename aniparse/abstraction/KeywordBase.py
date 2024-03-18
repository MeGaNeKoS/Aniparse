import logging
from dataclasses import dataclass, field
from typing import Set, Dict, Union

from aniparse.token_tags import Descriptor

logger = logging.getLogger(__name__)


@dataclass
class ElementEntry:
    word: str
    category_set: Set[Union[Descriptor]]
    regex_dict: Dict[str, Dict[int, Set[Descriptor]]] = field(default_factory=dict)
    # This work by checking if combined current word with the next word exists in the rule set or not.
    # If existed, then it will do the same check again with the next token.
    # Once it reaches the end of the rule set, it will add
    # the possibility to all the tokens it encounters during the check.
    # Every item in the set is a unique individual starting word combination
    continuation_set: Set[str] = field(default_factory=set)

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
