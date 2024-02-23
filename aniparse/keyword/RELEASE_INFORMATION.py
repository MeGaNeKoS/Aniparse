from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

release_information_prefix = [
    ElementEntry('BATCH', {Label.RELEASE_INFORMATION}),
    ElementEntry('COMPLETE', {Label.RELEASE_INFORMATION}),
    ElementEntry('PATCH', {Label.RELEASE_INFORMATION}),
    ElementEntry('REMUX', {Label.RELEASE_INFORMATION}),
    ElementEntry('END', {Label.RELEASE_INFORMATION}),
    ElementEntry('FINAL', {Label.RELEASE_INFORMATION}),
    ElementEntry('REMASTER', {Label.RELEASE_INFORMATION}),
    ElementEntry('REMASTERED', {Label.RELEASE_INFORMATION}),
    ElementEntry('UNCENSORED', {Label.RELEASE_INFORMATION}),
    ElementEntry('UNCUT', {Label.RELEASE_INFORMATION}),
    ElementEntry('TS', {Label.RELEASE_INFORMATION}),
    ElementEntry('VFR', {Label.RELEASE_INFORMATION}),
    ElementEntry('WIDESCREEN', {Label.RELEASE_INFORMATION}),
    ElementEntry('WS', {Label.RELEASE_INFORMATION}),
]
