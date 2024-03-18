from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

volume_prefix = [
    ElementEntry('VOL', {Descriptor.VOLUME}, regex_dict={r'VOL\.?': {0: {Descriptor.VOLUME}}}),
    ElementEntry('VOLUME', {Descriptor.VOLUME}, regex_dict={r'VOLUME\.?': {0: {Descriptor.VOLUME}}}),
]
