from aniparse.abstraction.KeywordBase import ElementEntry
from aniparse.token_tags import Descriptor

video_term_prefix = [
    ElementEntry('HI', set(),
                 regex_dict={r'HI(\d{2}P?)': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('H', set(),
                 regex_dict={r'H[\W_]?26[45]': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('X', set(),
                 regex_dict={r'X\.?26[45]': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('HEVC', {Descriptor.VIDEO_TERM},
                 regex_dict={r'HEVC2?': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('DIVX', {Descriptor.VIDEO_TERM},
                 regex_dict={r'DIVX[56]?': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('WMV', {Descriptor.VIDEO_TERM},
                 regex_dict={r'WMV[39]?': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('HQ', {Descriptor.VIDEO_TERM}),
    ElementEntry('LQ', {Descriptor.VIDEO_TERM}),
    ElementEntry('HD', {Descriptor.VIDEO_TERM}),
    ElementEntry('SD', {Descriptor.VIDEO_TERM}),
    ElementEntry('AVI', {Descriptor.VIDEO_TERM}),
    ElementEntry('AV1', {Descriptor.VIDEO_TERM}),
    ElementEntry('RMVB', {Descriptor.VIDEO_TERM}),
    ElementEntry('AVC', {Descriptor.VIDEO_TERM}),
    ElementEntry('XVID', {Descriptor.VIDEO_TERM})
]

video_term_suffix = [
    ElementEntry('FPS', set(),
                 regex_dict={r'\d{1,3}(\.\d{1,3})?FPS': {0: {Descriptor.VIDEO_TERM}}}),
    ElementEntry('BIT', set(),
                 regex_dict={r'\d{1,2}[\W_]?BITS?': {0: {Descriptor.VIDEO_TERM}}}),
]
