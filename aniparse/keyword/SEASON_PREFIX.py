from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

season_prefix = [
    ElementEntry('SAISON', {Descriptor.SEASON}),
    ElementEntry('SEASON', {Descriptor.SEASON}),
    ElementEntry('S', {Descriptor.SEASON}),
    ElementEntry("COUR", {Descriptor.SEASON}),
]
