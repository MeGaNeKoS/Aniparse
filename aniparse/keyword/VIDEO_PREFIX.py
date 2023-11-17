from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

volume_prefix = [
    ElementEntry('VOL', {DescriptorType.VOLUME_PREFIX}, regex_dict={r'VOL\.?': {0: {DescriptorType.VOLUME_PREFIX}}}),
    ElementEntry('VOLUME', {DescriptorType.VOLUME_PREFIX},
                 regex_dict={r'VOLUME\.?': {0: {DescriptorType.VOLUME_PREFIX}}}),
]
