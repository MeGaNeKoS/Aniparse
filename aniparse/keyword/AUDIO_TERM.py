from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

audio_term = [
    # Audio channels
    ElementEntry(word='CH', categories={Tag.AUDIO_TERM}, regex_dict={
        r'[2-9](\.\d{1,2}){1,2}(CH)?': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='DTS', categories={Tag.AUDIO_TERM}, regex_dict={
        r'DTS(?:[\W_]?(?:ES|HD[\W_]?(?:MA|HR)?))?': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='TRUEHD', categories={Tag.AUDIO_TERM}, regex_dict={
        r'TRUE[\W_]?HD[\W_]?\d{1,2}(\.\d{1,2}){0,2}\W?(CH)?': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='TRUE', categories=set(), regex_dict={
        r'TRUE[\W_]?HD[\W_]?\d{1,2}(\.\d{1,2}){0,2}\W?(CH)?': {0: {Tag.AUDIO_TERM}}
    }),

    # Audio codec
    ElementEntry(word='AAC', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='AACX', categories=set(), regex_dict={
        r'AACX[\W_]?\d{1,2}': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='AC', categories=set(), regex_dict={
        r'AC[\W_]?3': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='AC3', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='DD', categories=set(), regex_dict={
        r'DD[\W_]?\d{1,2}(\.\d{1,2}){0,2}': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='EAC3', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='E', categories=set(), regex_dict={
        r'E[\W_]?AC\W?3': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='FLAC', categories={Tag.AUDIO_TERM}, regex_dict={
        r'FLAC\d\.\d': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='FLACX', categories={Tag.AUDIO_TERM}, regex_dict={
        r'FLACX[\W_]?\d{1,2}': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='LOSSLESS', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='MP', categories=set(), regex_dict={
        r'MP[\W_]?3': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='MP3', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='OGG', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='VORBIS', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='Opus', categories={Tag.AUDIO_TERM}),

    # MISC
    ElementEntry(word='DUAL', categories=set(), regex_dict={
        r'DUAL[\W_]?AUDIO': {0: {Tag.AUDIO_TERM}}
    }),
    ElementEntry(word='DUALAUDIO', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='MULTI', categories=set(), regex_dict={
        r'MULTI[\W_]?AUDIO': {0: {Tag.AUDIO_TERM}},
    }),
    ElementEntry(word='MULTIAUDIO', categories={Tag.AUDIO_TERM}),

    # Additional codecs
    ElementEntry(word='PCM', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='ALAC', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='WMA', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='ATMOS', categories={Tag.AUDIO_TERM}),
    ElementEntry(word='HE', categories=set(), regex_dict={
        r'HE[\W_]?AAC': {0: {Tag.AUDIO_TERM}}
    }),
]