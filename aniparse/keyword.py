import logging
import weakref

from aniparse.element import ElementCategory

__all__ = ['KeywordOption', 'Keyword']

logger = logging.getLogger(__name__)


class KeywordOption:
    """
    A class representing the options for a `Keyword`.

    The options for a `Keyword` include whether it is identifiable, searchable, and valid.

    Properties:
        identifiable: A boolean indicating whether the `Keyword` can be identified.
        searchable: A boolean indicating whether the `Keyword` can be searched for.
        valid: A boolean indicating whether the `Keyword` is valid.
    """

    _instances = weakref.WeakValueDictionary()

    def __new__(cls, identifiable: bool = True, searchable: bool = True, valid: bool = True):
        """
        Create a new instance of `KeywordOption` if it doesn't already exist.
        Otherwise, return the existing instance.
        """
        key = (identifiable, searchable, valid)
        if key in cls._instances:
            return cls._instances[key]

        instance = super().__new__(cls)
        cls._instances[key] = instance
        return instance

    def __init__(self, identifiable: bool = True, searchable: bool = True, valid: bool = True):
        """
        Initialize a `KeywordOption` instance with the given options.
        """
        self.__identifiable = identifiable
        self.__searchable = searchable
        self.__valid = valid

    @property
    def identifiable(self) -> bool:
        """
        A boolean indicating whether the `Keyword` can be identified.
        """
        return self.__identifiable

    @property
    def searchable(self) -> bool:
        """
        A boolean indicating whether the `Keyword` can be searched for.
        """
        return self.__searchable

    @property
    def valid(self) -> bool:
        """
        A boolean indicating whether the `Keyword` is valid.
        """
        return self.__valid


class Keyword:
    """
    A class representing a keyword in an anime filename.

    A keyword is an element in the filename that has a specific category (e.g. ANIME_SEASON, ANIME_TYPE, etc.) and a set of options (e.g. case sensitivity, searchable, etc.) that can be used to customize the parsing and search behavior of the element.

    Attributes:
    category (ElementCategory): The element category of the keyword (e.g. ANIME_SEASON, ANIME_TYPE, etc.).
    options (KeywordOption): The options for the keyword.
    """

    def __init__(self, category: ElementCategory, options: KeywordOption):
        self.category = category
        self.options = options
