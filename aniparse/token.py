import weakref
from collections import defaultdict
from enum import Enum, auto
from typing import Union, Iterator, Literal, List, Set, Dict

from aniparse.element import Label, Metadata

PossibilityAction = Literal['add', 'remove']


class Token:
    """
    A class representing a token in a filename.
    """

    def __init__(self, content: str, index: int, category: Label = Label.UNKNOWN):
        """
        Initializes a new Token instance.

        Parameters:
            content (str): The string content of the token,
            index (int): The character position of the token in the filename.
            category (ElementCategory, optional): The element category of the token. Defaults to ElementCategory.UNKNOWN.
        """
        self.content = content
        self.original = content
        self.index = index
        self._category = category
        self._possibilities: Dict[Label, int] = {}

        self._observers = weakref.WeakSet()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Token instance.
        """
        return (f"Token(\n"
                f"\tcontent=\"{self.content}\"\n"
                f"\tcategory=\"{self.category}\"\n"
                f"\tpossibilities={[pos for pos in self.possibilities]}\n)")

    @property
    def possibilities(self) -> Dict[Label, int]:
        """
        Get the possibilities of the token.

        Return:
            Iterator[Label]: The possibilities of the token.
        """
        return self._possibilities

    @possibilities.setter
    def possibilities(self, new_possibilities):
        raise AttributeError('Cannot set possibilities directly. Use add_possibility and remove_possibility instead.')

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        raise AttributeError('Cannot set category directly. Use add_possibility and remove_possibility instead.')
        # old_category = self._category
        # self._category = new_category
        # self._notify_category_observers(old_category)

    def add_possibility(self, possibilities: Union[Label, List[Label], Set[Label]]):
        """
        Adds one or more ElementCategory possibilities to the Token instance.
        """
        if not isinstance(possibilities, (list, set)):
            possibilities = [possibilities]

        for possibility in possibilities:
            if possibility not in self._possibilities:
                self._possibilities[possibility] = 0

        self._notify_possibilities_observers('add', possibilities)

    def remove_possibility(self, possibilities: Union[Label, List[Label], Metadata, List[Metadata]] = None):
        """
        Removes one or more ElementCategory possibilities from the Token instance.
        """
        if not possibilities:
            possibilities = list(self._possibilities.keys())
        elif not isinstance(possibilities, list):
            possibilities = [possibilities]


        for possibility in possibilities:
            self._possibilities.pop(possibility, None)

        self._notify_possibilities_observers('remove', possibilities)

    def _notify_category_observers(self, old_category: Label):
        """
        Notifies all observers of a changed ElementCategory category.
        """
        for observer in self._observers:
            observer.token_category_changed(self, old_category)

    def _notify_possibilities_observers(self, action: PossibilityAction, possibility):
        """
        Notifies all observers of an added or removed ElementCategory possibility.
        """
        for observer in self._observers:
            observer.token_possibilities_changed(self, action, possibility)

    def add_observer(self, observer: 'Tokens'):
        """
        Adds an observer to the Token instance.
        """
        self._observers.add(observer)

    def remove_observer(self, observer: 'Tokens'):
        """
        Removes an observer from the Token instance.
        """
        self._observers.discard(observer)


class Tokens:
    """
    A container for a list of tokens, each associated with one or more categories.

    Attributes:
        tokens (list): A list of `Token` objects.
        lookup_category (defaultdict): A dictionary that maps `ElementCategory` objects to lists
            of `Token` objects that belong to that category.
        lookup_possibilities (defaultdict): A dictionary that maps `ElementCategory` objects to lists
            of `Token` objects that can be used as that category.
    """

    def __init__(self):
        """
        Initialize a new `Tokens` object.
        """
        self.tokens: List[Token] = []
        self.lookup_category: dict[Label, list] = {}
        self.lookup_possibilities: dict[Label, list] = {}

    def __iter__(self) -> Iterator[Token]:
        return iter(self.tokens)

    def add_token(self, token: Token):
        """
        Add a token to the collection and update the lookup_category.

        This method appends the given token to the tokens list, updates the
        lookup_category dictionary, and adds the current instance as an observer
        for the token.

        Parameter:
            token (Token): The token to be added to the collection.
        """
        self.tokens.append(token)
        self.lookup_category.setdefault(token.category, []).append(token)
        token.add_observer(self)

    @staticmethod
    def find_in_tokens(
            tokens: list[Token],
            category_in: list[Label] = None,
            category_not_in: list[Label] = None,
            content_in: list[str] = None,
            content_not_in: list[str] = None) -> Union['Token', None]:
        """
        Find the next token in the token list.

        Parameters:
            tokens (list[Token]): The token list to search in.
            category_in (Label): The element category to search for.
            category_not_in (Label): The element category to exclude.

        Returns:
            Token: The next token in the token list.
            None: If no token is found.
        """
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
                  category_in: list[Label] = None,
                  category_not_in: list[Label] = None,
                  content_in: list[str] = None,
                  content_not_in: list[str] = None) -> Union['Token', None]:
        """
        Find the next token in the token list.

        Parameters:
            token (Token): The token to start searching from.
            category_in (Label): The element category to search for.
            category_not_in (Label): The element category to exclude.

        Returns:
            Token: The next token in the token list.
            None: If no token is found.
        """
        if token is not None:
            tokens = self.tokens[self.get_index(token) + 1:]
        else:
            tokens = self.tokens
        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def find_prev(self,
                  token: Token = None,
                  category_in: list[Label] = None,
                  category_not_in: list[Label] = None,
                  content_in: list[str] = None,
                  content_not_in: list[str] = None) -> Union['Token', None]:
        """
        Find the previous token in the token list.

        Parameters:
            token (Token): The token to start searching from.
            category_in (Label): The element category to search for.
            category_not_in (Label): The element category to exclude.

        Returns:
            Token: The previous token in the token list.
            None: If no token is found.
        """
        if token is None:
            tokens = self.tokens[::-1]
        else:
            tokens = self.tokens[:self.get_index(token)][::-1]

        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def find_in_between(self,
                        start_token: Token = None,
                        end_token: Token = None,
                        category_in: list[Label] = None,
                        category_not_in: list[Label] = None,
                        content_in: list[str] = None,
                        content_not_in: list[str] = None) -> Union['Token', None]:
        """
        Find a token between two specified tokens in the token list.

        Parameters:
            start_token (Token, optional): The token to start searching from.
            end_token (Token, optional): The token to end the search at.
            category_in (list[DescriptorType], optional): The element categories to search for.
            category_not_in (list[DescriptorType], optional): The element categories to exclude.
            content_in (list[str], optional): The content strings to search for.
            content_not_in (list[str], optional): The content strings to exclude.

        Returns:
            Token: A token between the specified start and end tokens that meets the filtering criteria.
            None: If no token is found.
        """
        start_index = self.get_index(start_token) + 1 if start_token is not None else 0
        end_index = self.get_index(end_token) if end_token is not None else len(self.tokens)

        if start_index >= end_index:
            return None

        tokens = self.tokens[start_index:end_index]
        return self.find_in_tokens(tokens, category_in, category_not_in, content_in, content_not_in)

    def get_categories(self, category: Label):
        """
        Retrieve tokens belonging to the specified category.

        Parameters:
            category (Label): The category to filter tokens by.

        Returns:
            list[Token]: A list of tokens in the specified category.
        """
        return self.lookup_category[category]

    def get_token(self, index: int) -> Union[Token, None]:
        """Retrieve the token by a given character position in the filename."""
        for token in self.tokens:
            if token.index == index:
                return token
        return None

    def get_index(self, token: Token) -> int:
        """
        Get the index of the given token in the tokens list.

        Parameters:
            token (Token): The token to find the index for.

        Returns:
            int: The index of the token in the tokens list.
        """
        return self.tokens.index(token)

    def insert(self, index: int, token: Token) -> None:
        """
        Insert a token at the specified index in the tokens list.

        Parameters:
            index (int): The index at which to insert the token.
            token (Token): The token to be inserted.
        """
        self.tokens.insert(index, token)
        self.lookup_category[token.category].append(token)
        token.add_observer(self)

    def insert_after(self, token: Token, new_token: Token) -> None:
        """
        Insert a new token immediately after the specified token in the tokens list.

        Parameters:
            token (Token): The token after which to insert the new token.
            new_token (Token): The new token to be inserted.
        """
        self.insert(self.get_index(token) + 1, new_token)

    def insert_before(self, token: Token, new_token: Token) -> None:
        """
        Insert a new token immediately before the specified token in the tokens list.

        Parameters:
            token (Token): The token before which to insert the new token.
            new_token (Token): The new token to be inserted.
        """
        self.insert(self.get_index(token), new_token)

    def loop_forward(self,
                     begin: Token = None,
                     end: Token = None,
                     category: Union[Label, list[Label]] = None) -> Iterator[Token]:
        """
        Iterate through the tokens list between the specified begin and end tokens, filtered by category.

        Parameters:
            begin (Token, optional): The starting token for the iteration. Defaults to None.
            end (Token, optional): The ending token for the iteration. Defaults to None.
            category (Union[ElementCategory, list[ElementCategory]], optional): The category or list of categories to filter tokens by. Defaults to None.

        Yields:
            Iterator[Token]: An iterator over the tokens in the specified range and category.
        """
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
                      category: Union[Label, list[Label]] = None) -> Iterator[Token]:
        """
        Iterate through the tokens list between the specified end and begin tokens in reverse order, filtered by category, excluding the end token.

        Parameters:
            end (Token, optional): The ending token for the iteration, excluded from the iteration. Defaults to None.
            begin (Token, optional): The starting token for the iteration. Defaults to None.
            category (Union[DescriptorType, list[DescriptorType]], optional): The category or list of categories to filter tokens by. Defaults to None.

        Yields:
            Iterator[Token]: An iterator over the tokens in the specified range and category, in reverse order.
        """
        end_index = self.get_index(end) if end else len(self.tokens)
        begin_index = self.get_index(begin) + 1 if begin else 0
        tokens = self.tokens[begin_index:end_index][::-1]  # Reverse the slice
        for token in tokens:
            if category:
                if isinstance(category, list):
                    if token.category not in category:
                        continue
                elif token.category != category:
                    continue
            yield token

    def remove_token(self, token: Token):
        """
        Remove a token from the tokens list and update the lookup_category.

        Parameters:
            token (Token): The token to be removed.
        """
        self.tokens.remove(token)
        self.lookup_category[token.category].remove(token)
        token.remove_observer(self)

    def token_category_changed(self, token: Token, old_category: Label):
        """
        Update the lookup_category when a token's category changes.

        Parameters:
            token (Token): The token whose category has changed.
            old_category (Label): The old category of the token.
        """
        self.lookup_category[old_category].remove(token)
        self.lookup_category[token.category].append(token)

    def token_possibilities_changed(self, token: Token,
                                    action: PossibilityAction,
                                    possibilities: list[Label]):
        """
        Update the lookup_possibilities when a token's possibilities change.

        Parameters:
            token (Token): The token whose possibilities have changed.
            action (PossibilitiesAction): The action performed on the token's possibilities ('add' or 'remove').
            possibilities (list[Label]): The list of ElementCategory possibilities that have been added or removed.
        """
        if action == 'add':
            for possibility in possibilities:
                self.lookup_possibilities.setdefault(possibility, []).append(token)
        elif action == 'remove':
            for possibility in possibilities:
                try:
                    self.lookup_possibilities.get(possibility, []).remove(token)
                except Exception:
                    pass
