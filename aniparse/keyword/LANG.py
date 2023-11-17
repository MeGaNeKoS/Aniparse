from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

language_prefix = [
    ElementEntry('ENG', {DescriptorType.LANGUAGE}),
    ElementEntry('ENGLISH', {DescriptorType.LANGUAGE}),
    ElementEntry('ESPANOL', {DescriptorType.LANGUAGE}),
    ElementEntry('JAP', {DescriptorType.LANGUAGE}),
    ElementEntry('PT', {DescriptorType.LANGUAGE}, regex_dict={r'PT[\W_]?BR': {0: {DescriptorType.LANGUAGE}}}),
    ElementEntry('PTBR', {DescriptorType.LANGUAGE}, regex_dict={r'PT[\W_]?BR': {0: {DescriptorType.LANGUAGE}}}),
    ElementEntry('SPANISH', {DescriptorType.LANGUAGE}),
    ElementEntry('VOSTFR', {DescriptorType.LANGUAGE}),
    ElementEntry('ESP', {DescriptorType.LANGUAGE}),
    ElementEntry('ITA', {DescriptorType.LANGUAGE})
]
