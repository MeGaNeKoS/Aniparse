from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

device_compatibility_prefix = [
    ElementEntry('IPAD', {Descriptor.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPAD\d+': {0: {Descriptor.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPHONE', {Descriptor.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPHONE\d+': {0: {Descriptor.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPOD', {Descriptor.DEVICE_COMPATIBILITY}),
    ElementEntry('PS', {Descriptor.DEVICE_COMPATIBILITY},
                 regex_dict={r'PS\d+': {0: {Descriptor.DEVICE_COMPATIBILITY}}}),
    ElementEntry('XBOX', {Descriptor.DEVICE_COMPATIBILITY},
                 regex_dict={r'XBOX\d+': {0: {Descriptor.DEVICE_COMPATIBILITY}}}),
    ElementEntry('ANDROID', {Descriptor.DEVICE_COMPATIBILITY}),
]
