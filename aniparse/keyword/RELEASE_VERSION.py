from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

release_version = [
    ElementEntry(
        word='V',
        categories=set(),
        regex_dict={r'(V)(\d{1,2})': {
            1: {Tag.CONTEXT_DELIMITER},
            2: {Tag.RELEASE_VERSION}
        }}
    ),
    ElementEntry(word='VER', categories={Tag.RELEASE_VERSION}),
    ElementEntry(word='VERSION', categories={Tag.RELEASE_VERSION}),
]
