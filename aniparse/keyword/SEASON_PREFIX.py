from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

season_prefix = [
    ElementEntry('SAISON', {DescriptorType.SEASON_PREFIX}),
    ElementEntry('SEASON', {DescriptorType.SEASON_PREFIX}),
    ElementEntry('S', {DescriptorType.SEASON_PREFIX}),
    ElementEntry("COUR", {DescriptorType.SEASON_PREFIX}),
]
