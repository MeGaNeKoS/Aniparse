from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

video_resolution = [
    ElementEntry(word='P', categories=set(), regex_dict={
        r'\d{3,4}p': {0: {Tag.VIDEO_RESOLUTION}}
    }),
    ElementEntry(word='I', categories=set(), regex_dict={
        r'\d{3,4}i': {0: {Tag.VIDEO_RESOLUTION}}
    }),
    ElementEntry(word='K', categories=set(), regex_dict={
        r'\dK': {0: {Tag.VIDEO_RESOLUTION}}
    }),
    ElementEntry(word='X', categories=set(), regex_dict={
        r'(\d{3,4}x\d{3,4})': {0: {Tag.VIDEO_RESOLUTION}}
    })
]
