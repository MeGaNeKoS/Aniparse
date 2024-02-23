from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

subs_term_prefix = [
    ElementEntry('ASS', {Label.SUBS_TERM}),
    ElementEntry('BIG', set(), continuation_set={"5"}),
    ElementEntry('DUB', {Label.SUBS_TERM}),
    ElementEntry('DUBBED', {Label.SUBS_TERM}),
    ElementEntry('HARDSUB', {Label.SUBS_TERM}),
    ElementEntry('HARDSUBS', {Label.SUBS_TERM}),
    ElementEntry('RAW', {Label.SUBS_TERM}),
    ElementEntry('SOFTSUB', {Label.SUBS_TERM}),
    ElementEntry('SOFTSUBS', {Label.SUBS_TERM}),
    ElementEntry('SUB', {Label.SUBS_TERM}),
    ElementEntry('SUBBED', {Label.SUBS_TERM}),
    ElementEntry('SUBTITLED', {Label.SUBS_TERM}),

    # MISC
    ElementEntry('DUAL', set(), regex_dict={
        r'DUAL[\W_]?SUB(S?|TITLES?)?': {0:{Label.SUBS_TERM}}
    }),
    ElementEntry('MULTI', set(), regex_dict={
        r'MULTI[\W_]?SUB(S?|TITLES?)?': {0:{Label.SUBS_TERM}}
    })
]
