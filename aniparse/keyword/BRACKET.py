import itertools

from aniparse import constant
from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

bracket_prefix = []
for word in itertools.chain(constant.OPEN_BRACKETS, constant.CLOSE_BRACKETS):
    bracket_prefix.append(ElementEntry(word, {Descriptor.BRACKET}))
