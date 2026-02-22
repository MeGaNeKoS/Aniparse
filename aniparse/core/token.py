from __future__ import annotations

import weakref
from typing import Union, Iterator, Literal, List, Set, Dict, Optional

from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

PossibilityAction = Literal['add', 'remove']


class Possibility:
    __slots__ = ('descriptor', 'score', 'element')

    def __init__(self, descriptor: Tag, score: float = 0.0, element: Optional[ElementEntry] = None):
        self.descriptor = descriptor
        self.score = score
        self.element = element

    def __repr__(self):
        return f"Possibility({self.descriptor.value}, score={self.score})"


class Token:
    """
    A class representing a token in a filename.
    """

    def __init__(self, content: str, index: int, category: Tag = Tag.UNKNOWN):
        self.content = content
        self.original = content
        self.index = index
        self._category = category
        self._possibilities: Dict[Tag, Possibility] = {}
        self._observers = weakref.WeakSet()
        self.zone: Optional[str] = None
        self.bracket_group = None  # Set by rhythm analysis (BracketGroup or None)
        self.split_boundary: bool = False  # Set by resplit — marks group break for compose

    def __repr__(self) -> str:
        return (f"Token(\n"
                f"\tcontent=\"{self.content}\"\n"
                f"\tcategory=\"{self.category}\"\n"
                f"\tpossibilities={[pos for pos in self.possibilities]}\n)")

    @property
    def possibilities(self) -> Dict[Tag, Possibility]:
        return self._possibilities

    @possibilities.setter
    def possibilities(self, new_possibilities):
        raise AttributeError('Cannot set possibilities directly. Use add_possibility and remove_possibility instead.')

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        raise AttributeError('Cannot set category directly.')

    def add_possibility(self, possibilities: Union[Tag, List[Tag], Set[Tag]],
                        element: Optional[ElementEntry] = None, base_score: float = 0.0):
        """Adds one or more possibilities to the token."""
        if not isinstance(possibilities, (list, set)):
            possibilities = [possibilities]

        for possibility in possibilities:
            label = possibility.group
            if label not in self._possibilities:
                self._possibilities[label] = Possibility(
                    descriptor=possibility,
                    score=base_score,
                    element=element,
                )
            elif base_score > self._possibilities[label].score:
                # Update score if higher (e.g., regex match overrides keyword match)
                self._possibilities[label] = Possibility(
                    descriptor=possibility,
                    score=base_score,
                    element=element or self._possibilities[label].element,
                )

        self._notify_possibilities_observers('add', possibilities)

    def remove_possibility(self, possibilities: Union[Tag, List[Tag]] = None):
        """Removes one or more possibilities from the token."""
        if not possibilities:
            possibilities = list(self._possibilities.keys())
        elif not isinstance(possibilities, list):
            possibilities = [possibilities]

        for possibility in possibilities:
            self._possibilities.pop(possibility, None)

        self._notify_possibilities_observers('remove', possibilities)

    def add_score(self, label: Tag, delta: float):
        """Add delta to score for a given label."""
        if label in self._possibilities:
            self._possibilities[label].score += delta

    def get_score(self, label: Tag) -> float:
        """Get the score for a given label, 0.0 if not present."""
        p = self._possibilities.get(label)
        return p.score if p else 0.0

    def get_best_possibility(self) -> Optional[tuple[Tag, Possibility]]:
        """Return (Label, Possibility) with highest score, or None."""
        if not self._possibilities:
            return None
        return max(self._possibilities.items(), key=lambda x: x[1].score)

    def _notify_category_observers(self, old_category: Tag):
        for observer in self._observers:
            observer.token_category_changed(self, old_category)

    def _notify_possibilities_observers(self, action: PossibilityAction, possibility):
        for observer in self._observers:
            observer.token_possibilities_changed(self, action, possibility)

    def add_observer(self, observer: 'Tokens'):
        self._observers.add(observer)

    def remove_observer(self, observer: 'Tokens'):
        self._observers.discard(observer)


class Tokens:
    """
    A container for a list of tokens, each associated with one or more categories.
    """

    def __init__(self):
        self.tokens: List[Token] = []
        self.lookup_category: dict[Tag, list] = {}
        self.lookup_possibilities: dict[Tag, list] = {}

    def __iter__(self) -> Iterator[Token]:
        return iter(self.tokens)

    def add_token(self, token: Token):
        self.tokens.append(token)
        self.lookup_category.setdefault(token.category, []).append(token)
        token.add_observer(self)

    @staticmethod
    def find_in_tokens(
            tokens: list[Token],
            category_in: list[Tag] = None,
            category_not_in: list[Tag] = None,
            content_in: list[str] = None,
            content_not_in: list[str] = None) -> Union['Token', None]:
        for token in tokens:
            if (category_in and token.category not in category_in
                    or category_not_in and token.category in category_not_in
                    or content_in and token.content not in content_in
                    or content_not_in and token.content in content_not_in):
                continue
            return token
        return None

    def find_next(self,
                  token: Token = None,
                  category_in: list[Tag] = None,
                  category_not_in: list[Tag] = None,
                  content_in: list[str] = None,
                  content_not_in: list[str] = None) -> Union['Token', None]:
        if token is not None:
            tokens = self.tokens[self.get_index(token) + 1:]
        else:
            tokens = self.tokens
        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def find_prev(self,
                  token: Token = None,
                  category_in: list[Tag] = None,
                  category_not_in: list[Tag] = None,
                  content_in: list[str] = None,
                  content_not_in: list[str] = None) -> Union['Token', None]:
        if token is None:
            tokens = self.tokens[::-1]
        else:
            tokens = self.tokens[:self.get_index(token)][::-1]
        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def find_in_between(self,
                        start_token: Token = None,
                        end_token: Token = None,
                        category_in: list[Tag] = None,
                        category_not_in: list[Tag] = None,
                        content_in: list[str] = None,
                        content_not_in: list[str] = None) -> Union['Token', None]:
        start_index = self.get_index(start_token) + 1 if start_token is not None else 0
        end_index = self.get_index(end_token) if end_token is not None else len(self.tokens)
        if start_index >= end_index:
            return None
        tokens = self.tokens[start_index:end_index]
        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def get_categories(self, category: Tag):
        return self.lookup_category[category]

    def get_token(self, index: int) -> Union[Token, None]:
        """Retrieve the token by a given character position in the filename."""
        for token in self.tokens:
            if token.index == index:
                return token
        return None

    def get_index(self, token: Token) -> int:
        return self.tokens.index(token)

    def insert(self, index: int, token: Token) -> None:
        self.tokens.insert(index, token)
        self.lookup_category[token.category].append(token)
        token.add_observer(self)

    def insert_after(self, token: Token, new_token: Token) -> None:
        self.insert(self.get_index(token) + 1, new_token)

    def insert_before(self, token: Token, new_token: Token) -> None:
        self.insert(self.get_index(token), new_token)

    def loop_forward(self,
                     begin: Token = None,
                     end: Token = None,
                     category: Union[Tag, list[Tag]] = None) -> Iterator[Token]:
        begin_index = self.get_index(begin) + 1 if begin else 0
        end_index = self.get_index(end) if end else len(self.tokens)
        tokens = self.tokens[begin_index:end_index]
        for token in tokens:
            if category:
                if token.category not in category:
                    continue
            yield token

    def loop_backward(self,
                      end: Token = None,
                      begin: Token = None,
                      category: Union[Tag, list[Tag]] = None) -> Iterator[Token]:
        end_index = self.get_index(end) if end else len(self.tokens)
        begin_index = self.get_index(begin) + 1 if begin else 0
        tokens = self.tokens[begin_index:end_index][::-1]
        for token in tokens:
            if category:
                if isinstance(category, list):
                    if token.category not in category:
                        continue
                elif token.category != category:
                    continue
            yield token

    def remove_token(self, token: Token):
        self.tokens.remove(token)
        self.lookup_category[token.category].remove(token)
        token.remove_observer(self)

    def token_category_changed(self, token: Token, old_category: Tag):
        self.lookup_category[old_category].remove(token)
        self.lookup_category[token.category].append(token)

    def token_possibilities_changed(self, token: Token,
                                    action: PossibilityAction,
                                    possibilities: list[Tag]):
        if action == 'add':
            for possibility in possibilities:
                self.lookup_possibilities.setdefault(possibility, []).append(token)
        elif action == 'remove':
            for possibility in possibilities:
                try:
                    self.lookup_possibilities.get(possibility, []).remove(token)
                except Exception:
                    pass
