from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

context_dependent_prefix = [
    ElementEntry(word='THE', categories={Tag.CONTEXT_DEPENDENT}),
    ElementEntry(word='PART', categories={Tag.CONTEXT_DEPENDENT}, regex_dict={
        r'PART(\d+)': {
            0: {Tag.CONTENT_IDENTIFIER},
            1: {Tag.SEQUENCE_NUMBER},
        },
    }),
    ElementEntry(word='+', categories={Tag.CONTEXT_DEPENDENT}),
    ElementEntry(word='&', categories={Tag.CONTEXT_DEPENDENT}),
]