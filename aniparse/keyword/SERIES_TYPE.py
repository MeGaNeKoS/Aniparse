from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

series_type_prefix = [
    ElementEntry('GEKIJOUBAN', {Label.SERIES_TYPE}),
    ElementEntry('MOVIE', {Label.SERIES_TYPE}),
    ElementEntry('MOVIES', {Label.SERIES_TYPE}),
    ElementEntry('OAD', {Label.SERIES_TYPE}),
    ElementEntry('OAV', {Label.SERIES_TYPE}),
    ElementEntry('OVAS', {Label.SERIES_TYPE}),
    ElementEntry('ONA', {Label.SERIES_TYPE}),
    ElementEntry('OVA', {Label.SERIES_TYPE}),
    ElementEntry('SPECIAL', {Label.SERIES_TYPE}),
    ElementEntry('SPECIALS', {Label.SERIES_TYPE}),
    ElementEntry('TV', {Label.SERIES_TYPE}),
    ElementEntry('SP', {Label.SERIES_TYPE}),
    # ElementEntry('ED', {Label.SERIES_TYPE}),
    # ElementEntry('ENDING', {Label.SERIES_TYPE}),
    # ElementEntry('NCED', {Label.SERIES_TYPE}),
    # ElementEntry('CLEAN', set(), regex_dict={r'CLEAN[-.\s]?(ENDING|OPENING)S?': {0:{Label.SERIES_TYPE}}}),
    # ElementEntry('OP', {Label.SERIES_TYPE}),
    # ElementEntry('OPENING', {Label.SERIES_TYPE}),
    # ElementEntry('NCOP', {Label.SERIES_TYPE}),
    # ElementEntry('PREVIEW', {Label.SERIES_TYPE}),
    # ElementEntry('PV', {Label.SERIES_TYPE})
]
