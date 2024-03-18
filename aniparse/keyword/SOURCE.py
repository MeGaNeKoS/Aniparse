from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

source_prefix = [
    ElementEntry('BD', {Descriptor.SOURCE}, regex_dict={r'BD[\W_]?RIP': {0: {Descriptor.SOURCE}}}),
    ElementEntry('BDRIP', {Descriptor.SOURCE}),
    ElementEntry('BLURAY', {Descriptor.SOURCE}),
    ElementEntry('BLU', set(), regex_dict={r'BLU[\W_]?RAY': {0: {Descriptor.SOURCE}}}),
    ElementEntry('DVD', {Descriptor.SOURCE}, regex_dict={
        r'DVD[\W_]?(([Rr]\d{1,2}[A-Za-z]{0,4}|[A-Za-z]{0,4})|RIP)': {0: {Descriptor.SOURCE}}
    }),

    ElementEntry('DVDRIP', {Descriptor.SOURCE}),
    ElementEntry('DVDSCR', {Descriptor.SOURCE}),
    ElementEntry('R', set(), regex_dict={r'R\d{1,}[A-Z]{0,4}': {0: {Descriptor.SOURCE}}}),
    ElementEntry('RIP', {Descriptor.SOURCE}),
    ElementEntry('HDTV', {Descriptor.SOURCE}),
    ElementEntry('TV', {Descriptor.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {Descriptor.SOURCE}}}),
    ElementEntry('TVRIP', {Descriptor.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {Descriptor.SOURCE}}}),
    ElementEntry('WEB', {Descriptor.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {Descriptor.SOURCE}}}),
    ElementEntry('WEBRIP', {Descriptor.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {Descriptor.SOURCE}}}),
]
