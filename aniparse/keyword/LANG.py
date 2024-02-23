from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

language_prefix = [
    ElementEntry('ENG', {Label.LANGUAGE}),
    ElementEntry('ENGLISH', {Label.LANGUAGE}),
    ElementEntry('ESPANOL', {Label.LANGUAGE}),
    ElementEntry('JAP', {Label.LANGUAGE}),
    ElementEntry('PT', {Label.LANGUAGE}, regex_dict={r'PT[\W_]?BR': {0: {Label.LANGUAGE}}}),
    ElementEntry('PTBR', {Label.LANGUAGE}, regex_dict={r'PT[\W_]?BR': {0: {Label.LANGUAGE}}}),
    ElementEntry('SPANISH', {Label.LANGUAGE}),
    ElementEntry('VOSTFR', {Label.LANGUAGE}),
    ElementEntry('ESP', {Label.LANGUAGE}),
    ElementEntry('ITA', {Label.LANGUAGE})
]
