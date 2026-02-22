from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.core.token_tags import Tag

video_term_prefix = [
    ElementEntry(word='HI', categories=set(), regex_dict={
        r'HI(\d{2}P?)': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='H', categories=set(), regex_dict={
        r'H[\W_]?26[45]': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='X', categories=set(), regex_dict={
        r'X\.?26[45]': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='HEVC', categories={Tag.VIDEO_TERM}, regex_dict={
        r'HEVC2?': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='DIVX', categories={Tag.VIDEO_TERM}, regex_dict={
        r'DIVX[\W_]?(\d(\.\d(\.\d)?)?)?': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='WMV', categories={Tag.VIDEO_TERM}, regex_dict={
        r'WMV[39]?': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='HQ', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='LQ', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='HD', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='SD', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='AVI', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='AV', categories=set(), regex_dict={
        r'AV[\W_]?1': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='AV1', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='RMVB', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='AVC', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='XVID', categories={Tag.VIDEO_TERM}),

    # Standalone codec entries (for when tokenizer keeps them as single tokens)
    ElementEntry(word='X264', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='X265', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='H264', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='H265', categories={Tag.VIDEO_TERM}),

    # Additional codecs
    ElementEntry(word='VP9', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='VP8', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='MPEG4', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='MPEG2', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='THEORA', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='PRORES', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='HDR', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='HDR10', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='DV', categories={Tag.VIDEO_TERM}),  # Dolby Vision
    ElementEntry(word='DOLBY', categories=set(), regex_dict={
        r'DOLBY[\W_]?VISION': {0: {Tag.VIDEO_TERM}}
    }),
]

video_term_suffix = [
    ElementEntry(word='FPS', categories=set(), regex_dict={  # Adjust max_length for possible decimals in FPS
        r'\d{1,3}(\.\d{1,3})?FPS': {0: {Tag.VIDEO_TERM}}
    }),
    ElementEntry(word='BIT', categories=set(), regex_dict={
        r'\d{1,2}[\W_]?BITS?': {0: {Tag.VIDEO_TERM}}
    }),

    # Common compound bit-depth tokens
    ElementEntry(word='8BIT', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='10BIT', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='12BIT', categories={Tag.VIDEO_TERM}),

    # Hi10p / Hi444pp
    ElementEntry(word='HI10P', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='HI10', categories={Tag.VIDEO_TERM}),
    ElementEntry(word='HI444PP', categories={Tag.VIDEO_TERM}),
]
