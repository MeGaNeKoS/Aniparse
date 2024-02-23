from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

release_version_prefix = [
    ElementEntry(
        'V',
        set(),
        regex_dict={r'(V)(\d{1,2})': {1: {Label.CONTEXT_DELIMITER},
                                      2: {Label.RELEASE_VERSION}}}),
]
