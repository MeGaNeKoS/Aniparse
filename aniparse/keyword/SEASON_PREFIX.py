from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

season_prefix = [
    ElementEntry(word='SAISON', categories={Tag.SEASON}),
    ElementEntry(word='SEASON', categories={Tag.SEASON}),
    ElementEntry(word='S', categories={Tag.SEASON}),
    ElementEntry(word='COUR', categories={Tag.SEASON}),
    ElementEntry(word='TEMPORADA', categories={Tag.SEASON}),  # Spanish
    ElementEntry(word='STAFFEL', categories={Tag.SEASON}),  # German
]
