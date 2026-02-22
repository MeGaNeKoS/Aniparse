from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

release_information = [
    ElementEntry(word='BATCH', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='COMPLETE', categories={Tag.RELEASE_INFORMATION}, regex_dict={
        r'COMPLETE[\W_]?VERSION': {0: {Tag.RELEASE_INFORMATION}}
    }),
    ElementEntry(word='PATCH', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='REMUX', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='END', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='FINAL', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='REMASTER', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='REMASTERED', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='UNCENSORED', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='UNCUT', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='TS', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='VFR', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='WIDESCREEN', categories={Tag.RELEASE_INFORMATION}),
    ElementEntry(word='WS', categories={Tag.RELEASE_INFORMATION}),  # Accommodate "WIDESCREEN"
]
