from aniparse import keyword
from aniparse.wordlist import InMemoryWordListProvider, WordListManager, Table

default_word_list_provider = InMemoryWordListProvider()
default_word_list_manager = WordListManager()
default_word_list_manager.add_provider(default_word_list_provider)

for word in keyword.DEFAULT_PREFIX_KEYWORD:
    default_word_list_provider.add_word(word, Table.PREFIX)

for word in keyword.DEFAULT_SUFFIX_KEYWORD:
    default_word_list_provider.add_word(word, Table.SUFFIX)

for word in keyword.DEFAULT_SPECIAL_KEYWORD:
    default_word_list_provider.add_word(word, Table.INFIX)


