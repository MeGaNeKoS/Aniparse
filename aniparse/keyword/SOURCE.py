from aniparse.element import Label
from aniparse.abstraction.KeywordBase import ElementEntry

source_prefix = [
    ElementEntry('BD', {Label.SOURCE}, regex_dict={r'BD[\W_]?RIP': {0: {Label.SOURCE}}}),
    ElementEntry('BDRIP', {Label.SOURCE}),
    ElementEntry('BLURAY', {Label.SOURCE}),
    ElementEntry('BLU', set(), regex_dict={r'BLU[\W_]?RAY': {0: {Label.SOURCE}}}),
    ElementEntry('DVD', {Label.SOURCE}, regex_dict={
        r'DVD[\W_]?(([Rr]\d{1,2}[A-Za-z]{0,4}|[A-Za-z]{0,4})|RIP)': {0: {Label.SOURCE}}
    }),

    ElementEntry('DVDRIP', {Label.SOURCE}),
    ElementEntry('R', set(), regex_dict={r'R\d{1,}[A-Z]{0,4}': {0: {Label.SOURCE}}}),
    ElementEntry('RIP', {Label.SOURCE}),
    ElementEntry('HDTV', {Label.SOURCE}),
    ElementEntry('TV', {Label.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {Label.SOURCE}}}),
    ElementEntry('TVRIP', {Label.SOURCE}, regex_dict={r'TV[\W_]?RIP': {0: {Label.SOURCE}}}),
    ElementEntry('WEB', {Label.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {Label.SOURCE}}}),
    ElementEntry('WEBRIP', {Label.SOURCE}, regex_dict={r'WEB[\W_]?(RIP|CAST)': {0: {Label.SOURCE}}}),
]
