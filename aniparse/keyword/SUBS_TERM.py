from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

subs_term_prefix = [
    ElementEntry(word='ASS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='BIG5', categories={Tag.SUBS_TERM}),
    ElementEntry(word='DUB', categories={Tag.SUBS_TERM}),  # Accommodate "DUBBED"
    ElementEntry(word='DUBBED', categories={Tag.SUBS_TERM}),
    ElementEntry(word='HARDSUB', categories={Tag.SUBS_TERM}),
    ElementEntry(word='HARDSUBS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='RAW', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SOFTSUB', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SOFTSUBS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SUB', categories={Tag.SUBS_TERM}), # Accommodate "SUBBED"
    ElementEntry(word='SUBBED', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SUBTITLE', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SUBTITLES', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SUBTITLED', categories={Tag.SUBS_TERM}),
    ElementEntry(word='MULTIPLE', categories=set(), regex_dict={
        r'MULTIPLE[\W_]?(SUBTITLES?|SUBS?)': {0: {Tag.SUBS_TERM}}
    }),

    # MISC
    ElementEntry(word='DUAL', categories=set(), regex_dict={
        r'DUAL[\W_]?(SUBTITLES?|SUBS?)': {0:{Tag.SUBS_TERM}}
    }),
    ElementEntry(word='DUALSUB', categories={Tag.SUBS_TERM}),
    ElementEntry(word='DUALSUBS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='MULTI', categories=set(), regex_dict={
        r'MULTI[\W_]?(SUBTITLES?|SUBS?)': {0:{Tag.SUBS_TERM}}
    }),
    ElementEntry(word='MULTISUB', categories={Tag.SUBS_TERM}),
    ElementEntry(word='MULTISUBS', categories={Tag.SUBS_TERM}),
    # Handle hyphenated forms: "multi-subs" — tokenizer splits on hyphens
    # so these are handled by the MULTI regex above when tokens aren't split,
    # but we need standalone entries for when they are split
    ElementEntry(word='SUBS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='SUBX', categories=set(), regex_dict={
        r'SUBX[\W_]?\d{1,2}': {0: {Tag.SUBS_TERM}}
    }),

    # Additional terms
    ElementEntry(word='SRT', categories={Tag.SUBS_TERM}),
    ElementEntry(word='VTT', categories={Tag.SUBS_TERM}),
    ElementEntry(word='PGS', categories={Tag.SUBS_TERM}),
    ElementEntry(word='CC', categories={Tag.SUBS_TERM}),  # Closed captions
    ElementEntry(word='SOFT', categories=set(), regex_dict={
        r'SOFT[\W_]?SUBS?': {0: {Tag.SUBS_TERM}}
    }),
]