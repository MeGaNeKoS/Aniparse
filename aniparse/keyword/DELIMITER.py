from aniparse import constant
from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.element import DescriptorType

delimiters = []
for char in constant.DELIMITERS:
    delimiters.append(ElementEntry(char, {DescriptorType.DELIMITER}))