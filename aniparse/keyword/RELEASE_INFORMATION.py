from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

release_information_prefix = [
    ElementEntry('BATCH', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('COMPLETE', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('PATCH', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('REMUX', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('END', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('FINAL', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('REMASTER', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('REMASTERED', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('UNCENSORED', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('UNCUT', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('TS', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('VFR', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('WIDESCREEN', {Descriptor.RELEASE_INFORMATION}),
    ElementEntry('WS', {Descriptor.RELEASE_INFORMATION}),
]
