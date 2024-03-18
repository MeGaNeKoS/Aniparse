from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

context_dependent_prefix = [
    ElementEntry('THE', {Descriptor.CONTEXT_DEPENDENT}),
    ElementEntry('PART', {Descriptor.CONTEXT_DEPENDENT}),
    ElementEntry("+", {Descriptor.CONTEXT_DEPENDENT})
]
