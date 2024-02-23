from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

device_compatibility_prefix = [
    ElementEntry('IPAD', {Label.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPAD\d+': {0: {Label.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPHONE', {Label.DEVICE_COMPATIBILITY},
                 regex_dict={r'IPHONE\d+': {0: {Label.DEVICE_COMPATIBILITY}}}),
    ElementEntry('IPOD', {Label.DEVICE_COMPATIBILITY}),
    ElementEntry('PS', {Label.DEVICE_COMPATIBILITY},
                 regex_dict={r'PS\d+': {0: {Label.DEVICE_COMPATIBILITY}}}),
    ElementEntry('XBOX', {Label.DEVICE_COMPATIBILITY},
                 regex_dict={r'XBOX\d+': {0: {Label.DEVICE_COMPATIBILITY}}}),
    ElementEntry('ANDROID', {Label.DEVICE_COMPATIBILITY}),
]
