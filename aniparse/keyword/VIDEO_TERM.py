from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

video_term_prefix = [
    ElementEntry('HI', set(),
                 regex_dict={r'HI(\d{2}P?)': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('H', set(),
                 regex_dict={r'H[\W_]?26[45]': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('X', set(),
                 regex_dict={r'X\.?26[45]': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('HEVC', {Label.VIDEO_TERM},
                 regex_dict={r'HEVC2?': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('DIVX', {Label.VIDEO_TERM},
                 regex_dict={r'DIVX[56]?': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('WMV', {Label.VIDEO_TERM},
                 regex_dict={r'WMV[39]?': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('HQ', {Label.VIDEO_TERM}),
    ElementEntry('LQ', {Label.VIDEO_TERM}),
    ElementEntry('HD', {Label.VIDEO_TERM}),
    ElementEntry('SD', {Label.VIDEO_TERM}),
    ElementEntry('AVI', {Label.VIDEO_TERM}),
    ElementEntry('RMVB', {Label.VIDEO_TERM}),
    ElementEntry('AVC', {Label.VIDEO_TERM}),
    ElementEntry('XVID', {Label.VIDEO_TERM})
]

video_term_suffix = [
    ElementEntry('FPS', set(),
                 regex_dict={r'\d{1,3}(\.\d{1,3})?FPS': {0: {Label.VIDEO_TERM}}}),
    ElementEntry('BIT', set(),
                 regex_dict={r'\d{1,2}[\W_]?BITS?': {0: {Label.VIDEO_TERM}}}),
]
