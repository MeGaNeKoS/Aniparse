import itertools

from aniparse.core import constant
from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

brackets = []
for word in itertools.chain(constant.OPEN_BRACKETS, constant.CLOSE_BRACKETS):
    brackets.append(ElementEntry(
        word=word,
        categories={Tag.BRACKET}
    ))

