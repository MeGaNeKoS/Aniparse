from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

context_dependent_prefix = [
    ElementEntry('THE', {DescriptorType.CONTEXT_DEPENDENT}),
    ElementEntry('PART', {DescriptorType.CONTEXT_DEPENDENT}),
    ElementEntry("+", {DescriptorType.CONTEXT_DEPENDENT})
]
