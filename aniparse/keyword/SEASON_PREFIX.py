from aniparse.element import Metadata
from aniparse.abstraction.KeywordBase import ElementEntry

season_prefix = [
    ElementEntry('SAISON', {Metadata.SEASON_PREFIX}),
    ElementEntry('SEASON', {Metadata.SEASON_PREFIX}),
    ElementEntry('S', {Metadata.SEASON_PREFIX}),
    ElementEntry("COUR", {Metadata.SEASON_PREFIX}),
]
