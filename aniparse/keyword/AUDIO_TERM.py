from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

audio_term_prefix = [
    # Audio channels
    ElementEntry('DTS', {DescriptorType.AUDIO_TERM},
                 regex_dict={r'DTS[\W_]?(:?ES)?': {0: {DescriptorType.AUDIO_TERM}}}),
    ElementEntry(
        'TRUEHD',
        {DescriptorType.AUDIO_TERM},
        regex_dict={
            r'TRUE[\W_]?HD[\W_]?\d{1,2}(\.\d{1,2}){0,2}\W?(CH)?': {0: {DescriptorType.AUDIO_TERM}}
        }
    ),
    ElementEntry(
        'TRUE',
        set(),
        regex_dict={
            r'TRUE[\W_]?HD[\W_]?\d{1,2}(\.\d{1,2}){0,2}\W?(CH)?': {0: {DescriptorType.AUDIO_TERM}}
        }
    ),
    # Audio codec
    ElementEntry('AAC', {DescriptorType.AUDIO_TERM}),
    ElementEntry('AACX', set(), regex_dict={r'AACX[\W_]?\d{1,2}': {0: {DescriptorType.AUDIO_TERM}}}),
    ElementEntry('AC', set(), continuation_set={'3'}),
    ElementEntry('AC3', {DescriptorType.AUDIO_TERM}, continuation_set={'3'}),
    ElementEntry('EAC', set(), continuation_set={'3'}),
    ElementEntry('EAC3', {DescriptorType.AUDIO_TERM}),
    ElementEntry('E', set(),
                 regex_dict={r'E[\W_]?AC\W?3': {0: {DescriptorType.AUDIO_TERM}}}),
    ElementEntry('FLAC', {DescriptorType.AUDIO_TERM}),
    ElementEntry('FLACX', {DescriptorType.AUDIO_TERM},
                 regex_dict={r'FLACX[\W_]?\d{1,2}': {0: {DescriptorType.AUDIO_TERM}}}),
    ElementEntry('LOSSLESS', {DescriptorType.AUDIO_TERM}),
    ElementEntry('MP', set(), continuation_set={"3"}),
    ElementEntry('MP3', {DescriptorType.AUDIO_TERM}),
    ElementEntry('OGG', {DescriptorType.AUDIO_TERM}),
    ElementEntry('VORBIS', {DescriptorType.AUDIO_TERM}),

    # MISC
    ElementEntry('DUAL', set(), regex_dict={
        r'DUAL[\W_]?AUDIO': {0: {DescriptorType.AUDIO_TERM}}
    }),
    ElementEntry('MULTI', set(), regex_dict={
        r'MULTI[\W_]?AUDIO': {0: {DescriptorType.AUDIO_TERM}},
    })
]

audio_term_suffix = [
    # Audio channels
    ElementEntry('CH', {DescriptorType.AUDIO_TERM},
                 regex_dict={r'\d{1,2}(\.\d{1,2}){0,2}(CH)?': {0: {DescriptorType.AUDIO_TERM}}}),
]
