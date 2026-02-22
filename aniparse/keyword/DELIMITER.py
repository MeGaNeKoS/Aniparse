from aniparse.core import constant
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

delimiters = []
for char in constant.DELIMITERS:
    delimiters.append(ElementEntry(
        word=char,
        categories={Tag.DELIMITER}
    ))
