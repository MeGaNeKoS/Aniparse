from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

series_type_prefix = [
    ElementEntry('GEKIJOUBAN', {Descriptor.SERIES_TYPE}),
    ElementEntry('MOVIE', {Descriptor.SERIES_TYPE}),
    ElementEntry('MOVIES', {Descriptor.SERIES_TYPE}),
    ElementEntry('OAD', {Descriptor.SERIES_TYPE}),
    ElementEntry('OAV', {Descriptor.SERIES_TYPE}),
    ElementEntry('OVAS', {Descriptor.SERIES_TYPE}),
    ElementEntry('ONA', {Descriptor.SERIES_TYPE}),
    ElementEntry('OVA', {Descriptor.SERIES_TYPE}),
    ElementEntry('SPECIAL', {Descriptor.SERIES_TYPE}),
    ElementEntry('SPECIALS', {Descriptor.SERIES_TYPE}),
    ElementEntry('TV', {Descriptor.SERIES_TYPE}),
    ElementEntry('SP', {Descriptor.SERIES_TYPE})
]
