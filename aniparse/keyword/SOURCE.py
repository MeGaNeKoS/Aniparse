from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

source_prefix = [
    ElementEntry(word='BD', categories={Tag.SOURCE}, regex_dict={
        r'BD[\W_]?RIP': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='BDRIP', categories={Tag.SOURCE}),
    ElementEntry(word='BLURAY', categories={Tag.SOURCE}),
    ElementEntry(word='BLU', categories=set(), regex_dict={
        r'BLU[\W_]?RAY': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='DVD', categories={Tag.SOURCE}, regex_dict={
        r'DVD[\W_]?([Rr]\d{1,2}|R(?:E?MUX|IP))': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='DVDRIP', categories={Tag.SOURCE}),
    ElementEntry(word='DVDSCR', categories={Tag.SOURCE}),
    ElementEntry(word='REMUX', categories={Tag.SOURCE}),
    ElementEntry(word='RIP', categories={Tag.SOURCE}),
    ElementEntry(word='HDTV', categories={Tag.SOURCE}),
    ElementEntry(word='TV', categories={Tag.SOURCE}, regex_dict={
        r'TV[\W_]?RIP': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='TVRIP', categories={Tag.SOURCE}, regex_dict={
        r'TV[\W_]?RIP': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='WEB', categories={Tag.SOURCE}, regex_dict={
        r'WEB[\W_]?(RIP|CAST|DL)': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='WEBRIP', categories={Tag.SOURCE}, regex_dict={
        r'WEB[\W_]?(RIP|CAST|DL)': {0: {Tag.SOURCE}}
    }),
    ElementEntry(word='DL', categories=set(), regex_dict={
        r'WEB[\W_]?DL': {0: {Tag.SOURCE}}
    }),

    # Streaming service tags (used as source identifiers)
    ElementEntry(word='CR', categories={Tag.RELEASE_INFORMATION}),  # Crunchyroll
    ElementEntry(word='AMZN', categories={Tag.SOURCE}),  # Amazon Prime
    ElementEntry(word='NF', categories={Tag.SOURCE}),  # Netflix
    ElementEntry(word='DSNP', categories={Tag.SOURCE}),  # Disney+
    ElementEntry(word='HIDI', categories={Tag.SOURCE}),  # HiDive
    ElementEntry(word='HIDIVE', categories={Tag.SOURCE}),
    ElementEntry(word='FUNI', categories={Tag.SOURCE}),  # Funimation
    ElementEntry(word='VRV', categories={Tag.SOURCE}),
    ElementEntry(word='HULU', categories={Tag.SOURCE}),
    ElementEntry(word='MAX', categories={Tag.SOURCE}),  # HBO Max
    ElementEntry(word='ABEMA', categories={Tag.SOURCE}),
    ElementEntry(word='ADN', categories={Tag.SOURCE}),  # Anime Digital Network
    ElementEntry(word='B-GLOBAL', categories={Tag.SOURCE}),  # Bilibili Global
    ElementEntry(word='BILI', categories={Tag.SOURCE}),  # Bilibili
]