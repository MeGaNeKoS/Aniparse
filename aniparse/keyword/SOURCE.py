from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

source_prefix = [
    ElementEntry('BD', {DescriptorType.SOURCE}, regex_dict={r'BD[\W_]?RIP': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('BDRIP', {DescriptorType.SOURCE}),
    ElementEntry('BLURAY', {DescriptorType.SOURCE}),
    ElementEntry('BLU', set(), regex_dict={r'BLU[\W_]?RAY': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('DVD', {DescriptorType.SOURCE}, regex_dict={
        r'DVD[\W_]?(([Rr]\d{1,2}[A-Za-z]{0,4}|[A-Za-z]{0,4})|RIP)': {0: {DescriptorType.SOURCE}}
    }),

    ElementEntry('DVDRIP', {DescriptorType.SOURCE}),
    ElementEntry('R', set(), regex_dict={r'R\d{1,}[A-Z]{0,4}': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('RIP', {DescriptorType.SOURCE}),
    ElementEntry('HDTV', {DescriptorType.SOURCE}),
    ElementEntry('TV', {DescriptorType.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('TVRIP', {DescriptorType.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('WEB', {DescriptorType.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {DescriptorType.SOURCE}}}),
    ElementEntry('WEBRIP', {DescriptorType.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {DescriptorType.SOURCE}}}),
]
