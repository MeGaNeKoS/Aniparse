from aniparse import constant
from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.token_tags import Descriptor

delimiters = []
for char in constant.DELIMITERS:
    delimiters.append(ElementEntry(char, {Descriptor.DELIMITER})
                      )
