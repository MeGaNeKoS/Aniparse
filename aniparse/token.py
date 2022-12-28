from enum import Enum
from typing import Union

from aniparse.element import ElementCategory


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

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    UNKNOWN = ()
    BRACKET = ()
    DELIMITER = ()
    IDENTIFIER = ()
    INVALID = ()

    def __contains__(self, item: 'TokenType') -> bool:
        """
        Check if the given element category is equal to this element category.

        :param item: The element category to check.
        :return: True if the categories are equal, False otherwise.
        """
        return self.value == item.value


class Token:
    """
    A class representing a token in a filename.

    Parameters:
        content (str): The string content of the token.
        _type (TokenType): The category of the token (e.g. UNKNOWN, BRACKET, DELIMITER, IDENTIFIER, INVALID).
        category (ElementCategory): The element category of the token (e.g. ANIME_SEASON, ANIME_TITLE, etc.).
        enclosed (bool): Whether the token is enclosed in brackets.
    """

    def __init__(self, content: str = None, _type: TokenType = TokenType.UNKNOWN,
                 category: ElementCategory = ElementCategory.UNKNOWN, enclosed: bool = False):
        self.type = _type
        self.content = content
        self.enclosed = enclosed
        self.category = category
        self.prev = None
        self.next = None

    def find_next(self, type_in: TokenType = None, type_not_in: TokenType = None,
                  category_in: ElementCategory = None, category_not_in: ElementCategory = None) -> Union['Token', None]:
        """
        Find the next token in the token list.
        """
        token = self.next
        while token:
            if (type_in and token.type not in type_in
                    or type_not_in and token.type in type_not_in
                    or category_in and token.category not in category_in
                    or category_not_in and token.category in category_not_in):
                token = token.next
                continue

            return token
        return None

    def find_prev(self, type_in: TokenType = None, type_not_in: TokenType = None,
                  category_in: ElementCategory = None, category_not_in: ElementCategory = None) -> Union['Token', None]:
        """
        Find the previous token in the token list.
        """
        token = self.prev
        while token:
            if (type_in and token.type not in type_in
                    or type_not_in and token.type in type_not_in
                    or category_in and token.category not in category_in
                    or category_not_in and token.category in category_not_in):
                token = token.prev
                continue

            return token
        return None


class Tokens:
    """
    A class representing a doubly linked list of `Token` objects.
    """

    def __init__(self):
        """
        Initialize a new `Tokens` object.
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __bool__(self):
        return self.size > 0

    def __len__(self):
        return self.size

    def append(self, token: Token) -> None:
        """
        Append a new token to the end of the `Tokens` linked list.

        Args:
            token (Token): The token to append to the linked list.

        Returns:
            None: This method modifies the linked list in place and does not return anything.
        """
        if self.tail is None:
            self.head = self.tail = token
        else:
            self.tail.next = token
            token.prev = self.tail
            self.tail = token
        self.size += 1

    def combine(self, start_token: Token, end_token: Token, category: ElementCategory):
        """
        Combine the tokens between the start until the end tokens into a single token with the given category.

        Args:
            start_token (Token): The start token.
            end_token (Token): The end token.
            category (ElementCategory): The category to assign to the combined token.

        Returns:
            None: This method modifies the linked list in place and does not return anything.
        """
        if not start_token:
            return

        if start_token.next == end_token:
            return

        if end_token:
            end_token = end_token.next

        start_token.category = category

        if start_token.next:
            for token in self.loop_forward(start_token.next, end_token):
                start_token.content += token.content
                self.remove(token)

    def extend(self, other_tokens: 'Tokens') -> None:
        """
        Append the tokens from the given `Tokens` object to the current `Tokens` object.

        Args:
        - other_tokens (Tokens): The `Tokens` object to append to the current object.
        """
        if other_tokens.size == 0:
            return

        if self.size == 0:
            self.head = other_tokens.head
            self.tail = other_tokens.tail
            self.size = other_tokens.size
            return

        self.tail.next = other_tokens.head
        other_tokens.head.prev = self.tail
        self.tail = other_tokens.tail
        self.size += other_tokens.size

    def insert_after(self, token: Token, new_token: Token) -> None:
        """
        Insert a new token after the given token in the linked list.

        Args:
            token (Token): The token to insert the new token after.
            new_token (Token): The new token to be inserted.

        Returns:
            None: This method modifies the linked list in place and does not return anything.
        """
        new_token.prev = token
        new_token.next = token.next
        if token.next is None:
            self.tail = new_token
        else:
            token.next.prev = new_token
        token.next = new_token
        self.size += 1

    def insert_before(self, token: Token, new_token: Token) -> None:
        """
        Insert a new token before the given token in the linked list.

        Args:
            token (Token): The token to insert the new token before.
            new_token (Token): The new token to be inserted.

        Returns:
            None: This method modifies the linked list in place and does not return anything.
        """
        new_token.prev = token.prev
        new_token.next = token
        if token.prev is None:
            self.head = new_token
        else:
            token.prev.next = new_token
        token.prev = new_token
        self.size += 1

    def remove(self, token: Token) -> None:
        """
        Remove a token from the token list.

        Args:
        - token (Token): The token to remove from the list.

        Returns:
        None: This method modifies the token list in place and does not return anything.
        """
        if token.prev is None:
            self.head = token.next
        else:
            token.prev.next = token.next
        if token.next is None:
            self.tail = token.prev
        else:
            token.next.prev = token.prev
        self.size -= 1

    def loop_backward(self, current: Token = None, end: Token = None):
        """
        Iterate through the tokens in the list in reverse order, starting from the `current` token.
        If `current` is not provided, the iteration will start from the last token in the list.
        The iteration will continue until it reaches the `end` token, or until the head of the list is reached.

        Args:
            current (Token, optional): The token to start the iteration from. If not provided,
                the iteration will start from the last token in the list.
            end (Token, optional): The token at which to end the iteration. If not provided,
                the iteration will continue until the start of the list is reached.

        Yields:
            Token: The prev token in the list.
        """
        if current is None:
            current = self.tail

        while current is not end and current is not None:
            yield current
            current = current.prev

    def loop_forward(self, current: Token = None, end: Token = None):
        """
        Iterate through the tokens in the list, starting from the `current` token.
        If `current` is not provided, the iteration will start from the head token in the list.
        The iteration will continue until it reaches the `end` token, or until the tail of the list is reached.

        Args:
            current (Token, optional): The token to start the iteration from. If not provided,
                the iteration will start from the last token in the list.
            end (Token, optional): The token at which to end the iteration. If not provided,
                the iteration will continue until the start of the list is reached.

        Yields:
            Token: The next token in the list.
        """
        if current is None:
            current = self.head

        while current is not end and current is not None:
            yield current
            current = current.next
