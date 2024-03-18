from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

subs_term_prefix = [
    ElementEntry('ASS', {Descriptor.SUBS_TERM}),
    ElementEntry('BIG', set(), continuation_set={"5"}),
    ElementEntry('BIG5', {Descriptor.SUBS_TERM}),
    ElementEntry('DUB', {Descriptor.SUBS_TERM}),
    ElementEntry('DUBBED', {Descriptor.SUBS_TERM}),
    ElementEntry('HARDSUB', {Descriptor.SUBS_TERM}),
    ElementEntry('HARDSUBS', {Descriptor.SUBS_TERM}),
    ElementEntry('RAW', {Descriptor.SUBS_TERM}),
    ElementEntry('SOFTSUB', {Descriptor.SUBS_TERM}),
    ElementEntry('SOFTSUBS', {Descriptor.SUBS_TERM}),
    ElementEntry('SUB', {Descriptor.SUBS_TERM}),
    ElementEntry('SUBBED', {Descriptor.SUBS_TERM}),
    ElementEntry('SUBTITLED', {Descriptor.SUBS_TERM}),

    # MISC
    ElementEntry('DUAL', set(), regex_dict={
        r'DUAL[\W_]?SUB(S?|TITLES?)?': {0:{Descriptor.SUBS_TERM}}
    }),
    ElementEntry('MULTI', set(), regex_dict={
        r'MULTI[\W_]?SUB(S?|TITLES?)?': {0:{Descriptor.SUBS_TERM}}
    })
]
