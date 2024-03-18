from aniparse import constant
from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.token_tags import Descriptor

context_delimiters = []
for char in constant.CONTEXT_DELIMITER:
    context_delimiters.append(ElementEntry(char, {Descriptor.CONTEXT_DELIMITER}))