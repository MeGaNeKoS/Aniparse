from aniparse import constant
from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.element import Label

context_delimiters = []
for char in constant.CONTEXT_DELIMITER:
    context_delimiters.append(ElementEntry(char, {Label.CONTEXT_DELIMITER}))