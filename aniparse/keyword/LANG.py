from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

language_prefix = [
    ElementEntry('ENG', {Descriptor.LANGUAGE}),
    ElementEntry('ENGLISH', {Descriptor.LANGUAGE}),
    ElementEntry('ESPANOL', {Descriptor.LANGUAGE}),
    ElementEntry('JAP', {Descriptor.LANGUAGE}),
    ElementEntry('PT', {Descriptor.LANGUAGE}, regex_dict={r'PT[\W_]?BR': {0: {Descriptor.LANGUAGE}}}),
    ElementEntry('PTBR', {Descriptor.LANGUAGE}),
    ElementEntry('SPANISH', {Descriptor.LANGUAGE}),
    ElementEntry('VOSTFR', {Descriptor.LANGUAGE}),
    ElementEntry('ESP', {Descriptor.LANGUAGE}),
    ElementEntry('ITA', {Descriptor.LANGUAGE})
]
