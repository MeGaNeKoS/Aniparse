from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

device_compatibility_prefix = [
    ElementEntry(word='IPAD', categories={Tag.DEVICE_COMPATIBILITY}, regex_dict={
        r'IPAD\d+': {0: {Tag.DEVICE_COMPATIBILITY}}
    }),
    ElementEntry(word='IPHONE', categories={Tag.DEVICE_COMPATIBILITY}, regex_dict={
        r'IPHONE\d+': {0: {Tag.DEVICE_COMPATIBILITY}}
    }),
    ElementEntry(word='IPOD', categories={Tag.DEVICE_COMPATIBILITY}),
    ElementEntry(word='PS', categories={Tag.DEVICE_COMPATIBILITY}, regex_dict={
        r'PS\d+': {0: {Tag.DEVICE_COMPATIBILITY}}
    }),
    ElementEntry(word='XBOX', categories={Tag.DEVICE_COMPATIBILITY}, regex_dict={
        r'XBOX\d+': {0: {Tag.DEVICE_COMPATIBILITY}}
    }),
    ElementEntry(word='ANDROID', categories={Tag.DEVICE_COMPATIBILITY}),
]
