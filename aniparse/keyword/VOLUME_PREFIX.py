from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

volume_prefix = [
    ElementEntry(word='VOL', categories={Tag.VOLUME}, regex_dict={
        r'VOL\.?': {0: {Tag.VOLUME}}
    }),
    ElementEntry(word='VOLUME', categories={Tag.VOLUME}, regex_dict={
        r'VOLUME\.?': {0: {Tag.VOLUME}}
    }),
]
