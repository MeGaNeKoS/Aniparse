from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

release_information_prefix = [
    ElementEntry('BATCH', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('COMPLETE', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('PATCH', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('REMUX', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('END', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('FINAL', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('REMASTER', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('REMASTERED', {DescriptorType.RELEASE_INFORMATION}),
    ElementEntry('UNCENSORED', {DescriptorType.RELEASE_INFORMATION}),
]
