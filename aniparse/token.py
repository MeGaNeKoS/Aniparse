import weakref
from collections import defaultdict
from enum import Enum, auto
from typing import Union, Iterator, Literal

from aniparse.element import ElementCategory

PossibilitiesAction = Literal['add', 'remove']


class TokenType(Enum):
    """
    An enumeration of token types used to classify lexical tokens in a source code.

    The token types include:
        - UNKNOWN: the token type is unknown or cannot be classified
        - BRACKET: the token is a bracket, such as '[' or ']'
        - DELIMITER: the token is a delimiter, such as ',' or ' '
        - IDENTIFIER: the token is an identifier if it already has a category.
        - INVALID: the token is invalid or unrecognized

    The token types are represented as instances of the `TokenType` class.
    """

    UNKNOWN = auto()  # Default token type
    BRACKET = auto()  # For brackets only
    DELIMITER = auto()  # For delimiters from the allowed delimiter list
    IDENTIFIER = auto()  # For tokens that already have a category
    INVALID = auto()  # For tokens that are invalid or unrecognized and need to be ignored

    def __contains__(self, item: 'TokenType') -> bool:
        """
        Check if the given element category is equal to this element category.

        Parameter:
            item: The element category to check.

        Return:
            Bool: True if the categories are equal, False otherwise.
        """
        return self.value == item.value


class Token:
    """
    A class representing a token in a filename.
    """

    def __init__(self, content: str = None, type_: TokenType = TokenType.UNKNOWN,
                 category: ElementCategory = ElementCategory.UNKNOWN, nest_level: int = 0):
        """
        Initializes a new Token instance.

        Parameters:
            content (str, optional): The string content of the token. Defaults to None.
            type_ (TokenType, optional): The category of the token. Defaults to TokenType.UNKNOWN.
            category (ElementCategory, optional): The element category of the token. Defaults to ElementCategory.UNKNOWN.
            nest_level (int, optional): Whether the token is enclosed in brackets. Defaults to 0.
        """
        self.type = type_
        self.content = content
        self.nest_level = nest_level
        self._category = category
        self._possibilities = set()

        self._observers = weakref.WeakSet()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Token instance.
        """
        return (f"Token(\n"
                f"\tcontent=\"{self.content}\"\n"
                f"\ttype=\"{self.type}\"\n"
                f"\tcategory=\"{self.category}\"\n"
                f"\tnest_level={self.nest_level}\n"
                f"\tpossibilities={[pos for pos in self.possibilities]}\n)")

    @property
    def possibilities(self) -> Iterator[ElementCategory]:
        """
        Get the possibilities of the token.

        Return:
            Iterator[ElementCategory]: The possibilities of the token.
        """
        return iter(self._possibilities)

    @possibilities.setter
    def possibilities(self, new_possibilities):
        raise AttributeError('Cannot set possibilities directly. Use add_possibility and remove_possibility instead.')

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        old_category = self._category
        self._category = new_category
        self._notify_category_observers(old_category)

    def add_possibility(self, possibilities: Union[ElementCategory, list[ElementCategory]]):
        """
        Adds one or more ElementCategory possibilities to the Token instance.
        """
        if not isinstance(possibilities, list):
            possibilities = [possibilities]

        self._possibilities.update(possibilities)
        self._notify_possibilities_observers('add', possibilities)

    def remove_possibility(self, possibilities: Union[ElementCategory, list[ElementCategory]] = None):
        """
        Removes one or more ElementCategory possibilities from the Token instance.
        """
        if not isinstance(possibilities, list):
            possibilities = [possibilities]
        elif not possibilities:
            possibilities = self._possibilities
        self._possibilities.difference_update(possibilities)
        self._notify_possibilities_observers('remove', possibilities)

    def _notify_category_observers(self, old_category: ElementCategory):
        """
        Notifies all observers of a changed ElementCategory category.
        """
        for observer in self._observers:
            observer.token_category_changed(self, old_category)

    def _notify_possibilities_observers(self, action: PossibilitiesAction, possibility):
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
        self.tokens = []
        self.lookup_category: defaultdict[ElementCategory, list] = defaultdict(list)
        self.lookup_possibilities: defaultdict[ElementCategory, list] = defaultdict(list)

    def __iter__(self):
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
        self.lookup_category[token.category].append(token)
        token.add_observer(self)

    @staticmethod
    def find_in_tokens(
            tokens: list[Token],
            type_in: list[TokenType] = None,
            type_not_in: list[TokenType] = None,
            category_in: list[ElementCategory] = None,
            category_not_in: list[ElementCategory] = None) -> Union['Token', None]:
        """
        Find the next token in the token list.

        Parameters:
            tokens (list[Token]): The token list to search in.
            type_in (TokenType): The token type to search for.
            type_not_in (TokenType): The token type to exclude.
            category_in (ElementCategory): The element category to search for.
            category_not_in (ElementCategory): The element category to exclude.

        Returns:
            Token: The next token in the token list.
            None: If no token is found.
        """
        for token in tokens:
            if (type_in and token.type not in type_in
                    or type_not_in and token.type in type_not_in
                    or category_in and token.category not in category_in
                    or category_not_in and token.category in category_not_in):
                continue

            return token
        return None

    def find_next(self,
                  token: Token = None,
                  type_in: list[TokenType] = None,
                  type_not_in: list[TokenType] = None,
                  category_in: list[ElementCategory] = None,
                  category_not_in: list[ElementCategory] = None) -> Union['Token', None]:
        """
        Find the next token in the token list.

        Parameters:
            token (Token): The token to start searching from.
            type_in (TokenType): The token type to search for.
            type_not_in (TokenType): The token type to exclude.
            category_in (ElementCategory): The element category to search for.
            category_not_in (ElementCategory): The element category to exclude.

        Returns:
            Token: The next token in the token list.
            None: If no token is found.
        """
        if token is not None:
            tokens = self.tokens[self.get_index(token) + 1:]
        else:
            tokens = self.tokens
        return self.find_in_tokens(tokens, type_in, type_not_in, category_in, category_not_in)

    def find_prev(self,
                  token: Token = None,
                  type_in: list[TokenType] = None,
                  type_not_in: list[TokenType] = None,
                  category_in: list[ElementCategory] = None,
                  category_not_in: list[ElementCategory] = None) -> Union['Token', None]:
        """
        Find the previous token in the token list.

        Parameters:
            token (Token): The token to start searching from.
            type_in (TokenType): The token type to search for.
            type_not_in (TokenType): The token type to exclude.
            category_in (ElementCategory): The element category to search for.
            category_not_in (ElementCategory): The element category to exclude.

        Returns:
            Token: The previous token in the token list.
            None: If no token is found.
        """
        if token is None:
            tokens = self.tokens[::-1]
        else:
            index = max(self.get_index(token) - 1, 0)
            tokens = self.tokens[index::-1]

        return self.find_in_tokens(tokens, type_in, type_not_in, category_in, category_not_in)

    def get_categories(self, category: ElementCategory):
        """
        Retrieve tokens belonging to the specified category.

        Parameters:
            category (ElementCategory): The category to filter tokens by.

        Returns:
            list[Token]: A list of tokens in the specified category.
        """
        return self.lookup_category[category]

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
                     category: Union[ElementCategory, list[ElementCategory]] = None) -> Iterator[Token]:
        """
        Iterate through the tokens list between the specified begin and end tokens, filtered by category.

        Parameters:
            begin (Token, optional): The starting token for the iteration. Defaults to None.
            end (Token, optional): The ending token for the iteration. Defaults to None.
            category (Union[ElementCategory, list[ElementCategory]], optional): The category or list of categories to filter tokens by. Defaults to None.

        Yields:
            Iterator[Token]: An iterator over the tokens in the specified range and category.
        """
        begin_index = 0 if begin is None else self.get_index(begin)
        end_index = len(self.tokens) if end is None else self.get_index(end)
        tokens = self.tokens[begin_index:end_index + 1]
        for token in tokens:
            if category:
                if token.category not in category:
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

    def token_category_changed(self, token: Token, old_category: ElementCategory):
        """
        Update the lookup_category when a token's category changes.

        Parameters:
            token (Token): The token whose category has changed.
            old_category (ElementCategory): The old category of the token.
        """
        self.lookup_category[old_category].remove(token)
        self.lookup_category[token.category].append(token)

    def token_possibilities_changed(self, token: Token,
                                    action: PossibilitiesAction,
                                    possibilities: list[ElementCategory]):
        """
        Update the lookup_possibilities when a token's possibilities change.

        Parameters:
            token (Token): The token whose possibilities have changed.
            action (PossibilitiesAction): The action performed on the token's possibilities ('add' or 'remove').
            possibilities (list[ElementCategory]): The list of ElementCategory possibilities that have been added or removed.
        """
        if action == 'add':
            for possibility in possibilities:
                self.lookup_possibilities[possibility].append(token)
        elif action == 'remove':
            for possibility in possibilities:
                self.lookup_possibilities[possibility].remove(token)
