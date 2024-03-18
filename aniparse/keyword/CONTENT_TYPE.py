from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.token_tags import Descriptor

content_type_prefix = [
    ElementEntry('ED', {Descriptor.CONTENT_TYPE}),
    ElementEntry('ENDING', {Descriptor.CONTENT_TYPE}),
    ElementEntry('NCED', {Descriptor.CONTENT_TYPE}),
    ElementEntry('CLEAN', set(), regex_dict={r'CLEAN[-.\s]?(ENDING|OPENING)S?': {0: {Descriptor.CONTENT_TYPE}}}),
    ElementEntry('OP', {Descriptor.CONTENT_TYPE}),
    ElementEntry('OPENING', {Descriptor.CONTENT_TYPE}),
    ElementEntry('NCOP', {Descriptor.CONTENT_TYPE}),
    ElementEntry('PREVIEW', {Descriptor.CONTENT_TYPE}),
    ElementEntry('PV', {Descriptor.CONTENT_TYPE})
]
