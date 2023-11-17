from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

release_version_prefix = [
    ElementEntry(
        'V',
        set(),
        regex_dict={r'(V)(\d{1,2})': {1: {DescriptorType.CONTEXT_DELIMITER},
                                      2: {DescriptorType.RELEASE_VERSION}}}),
]
