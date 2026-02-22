from aniparse.core import constant
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

context_delimiters = []
for char in constant.CONTEXT_DELIMITER:
    context_delimiters.append(ElementEntry(
        word=char,
        categories={Tag.CONTEXT_DELIMITER}
    ))
