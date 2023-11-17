from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

video_term_prefix = [
    ElementEntry('HI', set(),
                 regex_dict={r'HI(\d{2}P?)': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('H', set(),
                 regex_dict={r'H[\W_]?26[45]': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('X', set(),
                 regex_dict={r'X\.?26[45]': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('HEVC', {DescriptorType.VIDEO_TERM},
                 regex_dict={r'HEVC2?': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('DIVX', {DescriptorType.VIDEO_TERM},
                 regex_dict={r'DIVX[56]?': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('WMV', {DescriptorType.VIDEO_TERM},
                 regex_dict={r'WMV[39]?': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('HQ', {DescriptorType.VIDEO_TERM}),
    ElementEntry('LQ', {DescriptorType.VIDEO_TERM}),
    ElementEntry('HD', {DescriptorType.VIDEO_TERM}),
    ElementEntry('SD', {DescriptorType.VIDEO_TERM}),
    ElementEntry('AVI', {DescriptorType.VIDEO_TERM}),
    ElementEntry('RMVB', {DescriptorType.VIDEO_TERM}),
    ElementEntry('AVC', {DescriptorType.VIDEO_TERM}),
    ElementEntry('XVID', {DescriptorType.VIDEO_TERM})
]

video_term_suffix = [
    ElementEntry('FPS', set(),
                 regex_dict={r'\d{1,3}(\.\d{1,3})?FPS': {0: {DescriptorType.VIDEO_TERM}}}),
    ElementEntry('BIT', set(),
                 regex_dict={r'\d{1,2}[\W_]?BITS?': {0: {DescriptorType.VIDEO_TERM}}}),
]
