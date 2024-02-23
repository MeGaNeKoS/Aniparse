from aniparse.element import Label, Metadata
from aniparse.abstraction.KeywordBase import ElementEntry

volume_prefix = [
    ElementEntry('VOL', {Metadata.VOLUME_PREFIX}, regex_dict={r'VOL\.?': {0: {Metadata.VOLUME_PREFIX}}}),
    ElementEntry('VOLUME', {Metadata.VOLUME_PREFIX},
                 regex_dict={r'VOLUME\.?': {0: {Metadata.VOLUME_PREFIX}}}),
]
