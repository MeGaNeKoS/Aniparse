from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

release_version_prefix = [
    ElementEntry(
        'V',
        set(),
        regex_dict={r'(V)(\d{1,2})': {1: {Descriptor.CONTEXT_DELIMITER},
                                      2: {Descriptor.RELEASE_VERSION}}}),
]
