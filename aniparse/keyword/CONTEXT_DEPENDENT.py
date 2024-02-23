from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

context_dependent_prefix = [
    ElementEntry('THE', {Label.CONTEXT_DEPENDENT}),
    ElementEntry('PART', {Label.CONTEXT_DEPENDENT}),
    ElementEntry("+", {Label.CONTEXT_DEPENDENT})
]
