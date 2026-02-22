from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

content_type = [
    ElementEntry(word='ED', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='ENDING', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='NCED', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='CLEAN', categories=set(), regex_dict={
        r'CLEAN[-.\s]?(ENDING|OPENING)S?': {0: {Tag.CONTENT_TYPE}}
    }),
    ElementEntry(word='OP', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='OPENING', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='NCOP', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='PREVIEW', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='PV', categories={Tag.CONTENT_TYPE}),
    ElementEntry(word='PILOT', categories={Tag.CONTENT_TYPE})
]
