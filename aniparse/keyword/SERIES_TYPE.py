from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

series_type = [
    ElementEntry(word='GEKIJOUBAN', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='MOVIE', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='MOVIES', categories={Tag.SERIES_TYPE}, canonical='Movie'),
    ElementEntry(word='OAD', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='OAV', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='OVAS', categories={Tag.SERIES_TYPE}, canonical='OVA'),
    ElementEntry(word='ONA', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='OVA', categories={Tag.SERIES_TYPE}),  # Accommodate "OAV"
    ElementEntry(word='SPECIAL', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='SPECIALS', categories={Tag.SERIES_TYPE}, canonical='Special'),
    ElementEntry(word='TV', categories={Tag.SERIES_TYPE}),
    ElementEntry(word='SP', categories={Tag.SERIES_TYPE}),  # Accommodate "SPECIAL"
]
