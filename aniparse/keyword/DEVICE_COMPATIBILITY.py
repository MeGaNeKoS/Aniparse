from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

device_compatibility_prefix = [
    ElementEntry('IPAD', {DescriptorType.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPAD\d+': {0: {DescriptorType.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPHONE', {DescriptorType.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPHONE\d+': {0: {DescriptorType.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPOD', {DescriptorType.DEVICE_COMPATIBILITY}),
    ElementEntry('PS', {DescriptorType.DEVICE_COMPATIBILITY},
                 regex_dict={r'PS\d+': {0: {DescriptorType.DEVICE_COMPATIBILITY}}}),
    ElementEntry('XBOX', {DescriptorType.DEVICE_COMPATIBILITY},
                 regex_dict={r'XBOX\d+': {0: {DescriptorType.DEVICE_COMPATIBILITY}}}),
    ElementEntry('ANDROID', {DescriptorType.DEVICE_COMPATIBILITY}),
]
