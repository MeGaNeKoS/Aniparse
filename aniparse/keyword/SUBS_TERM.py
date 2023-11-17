from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

subs_term_prefix = [
    ElementEntry('ASS', {DescriptorType.SUBS_TERM}),
    ElementEntry('BIG', set(), continuation_set={"5"}),
    ElementEntry('DUB', {DescriptorType.SUBS_TERM}),
    ElementEntry('DUBBED', {DescriptorType.SUBS_TERM}),
    ElementEntry('HARDSUB', {DescriptorType.SUBS_TERM}),
    ElementEntry('HARDSUBS', {DescriptorType.SUBS_TERM}),
    ElementEntry('RAW', {DescriptorType.SUBS_TERM}),
    ElementEntry('SOFTSUB', {DescriptorType.SUBS_TERM}),
    ElementEntry('SOFTSUBS', {DescriptorType.SUBS_TERM}),
    ElementEntry('SUB', {DescriptorType.SUBS_TERM}),
    ElementEntry('SUBBED', {DescriptorType.SUBS_TERM}),
    ElementEntry('SUBTITLED', {DescriptorType.SUBS_TERM}),

    # MISC
    ElementEntry('DUAL', set(), regex_dict={
        r'DUAL[\W_]?SUB(S?|TITLES?)?': {0:{DescriptorType.SUBS_TERM}}
    }),
    ElementEntry('MULTI', set(), regex_dict={
        r'MULTI[\W_]?SUB(S?|TITLES?)?': {0:{DescriptorType.SUBS_TERM}}
    })
]
