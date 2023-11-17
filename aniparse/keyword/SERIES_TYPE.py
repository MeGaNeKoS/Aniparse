from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

series_type_prefix = [
    ElementEntry('GEKIJOUBAN', {DescriptorType.SERIES_TYPE}),
    ElementEntry('MOVIE', {DescriptorType.SERIES_TYPE}),
    ElementEntry('MOVIES', {DescriptorType.SERIES_TYPE}),
    ElementEntry('OAD', {DescriptorType.SERIES_TYPE}),
    ElementEntry('OAV', {DescriptorType.SERIES_TYPE}),
    ElementEntry('OVAS', {DescriptorType.SERIES_TYPE}),
    ElementEntry('ONA', {DescriptorType.SERIES_TYPE}),
    ElementEntry('OVA', {DescriptorType.SERIES_TYPE}),
    ElementEntry('SPECIAL', {DescriptorType.SERIES_TYPE}),
    ElementEntry('SPECIALS', {DescriptorType.SERIES_TYPE}),
    ElementEntry('TV', {DescriptorType.SERIES_TYPE}),
    ElementEntry('SP', {DescriptorType.SERIES_TYPE}),
    ElementEntry('ED', {DescriptorType.SERIES_TYPE}),
    ElementEntry('ENDING', {DescriptorType.SERIES_TYPE}),
    ElementEntry('NCED', {DescriptorType.SERIES_TYPE}),
    ElementEntry('CLEAN', set(), regex_dict={r'CLEAN[-.\s]?(ENDING|OPENING)S?': {0:{DescriptorType.SERIES_TYPE}}}),
    ElementEntry('OP', {DescriptorType.SERIES_TYPE}),
    ElementEntry('OPENING', {DescriptorType.SERIES_TYPE}),
    ElementEntry('NCOP', {DescriptorType.SERIES_TYPE}),
    ElementEntry('PREVIEW', {DescriptorType.SERIES_TYPE}),
    ElementEntry('PV', {DescriptorType.SERIES_TYPE})
]
