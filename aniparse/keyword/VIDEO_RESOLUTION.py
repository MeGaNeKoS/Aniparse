from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

video_resolution_suffix = [
    ElementEntry('P', set(),
                 regex_dict={r'\d{3,4}p': {0: {Descriptor.VIDEO_RESOLUTION}}}),
    ElementEntry('I', set(),
                 regex_dict={r'\d{3,4}i': {0: {Descriptor.VIDEO_RESOLUTION}}}),
    ElementEntry('K', set(),
                 regex_dict={r'\dK': {0: {Descriptor.VIDEO_RESOLUTION}}}),
]

video_resolution_infix = [
    ElementEntry('X', set(),
                 regex_dict={r'(\d{3,4}x\d{3,4})': {0: {Descriptor.VIDEO_RESOLUTION}}})
]