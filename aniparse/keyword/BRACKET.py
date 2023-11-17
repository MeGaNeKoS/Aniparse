import itertools

from aniparse import constant
from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

bracket_prefix = []
for word in itertools.chain(constant.OPEN_BRACKETS, constant.CLOSE_BRACKETS):
    bracket_prefix.append(ElementEntry(word, {DescriptorType.BRACKET}))
