from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

language = [
    # ISO 639-2 three-letter codes (the standard in media tagging)
    # Users can extend via custom wordlist for less common languages
    ElementEntry(word='ENG', categories={Tag.LANGUAGE}),
    ElementEntry(word='JPN', categories={Tag.LANGUAGE}),
    ElementEntry(word='JAP', categories={Tag.LANGUAGE}),
    ElementEntry(word='CHI', categories={Tag.LANGUAGE}),
    ElementEntry(word='KOR', categories={Tag.LANGUAGE}),
    ElementEntry(word='SPA', categories={Tag.LANGUAGE}),
    ElementEntry(word='FRE', categories={Tag.LANGUAGE}),
    ElementEntry(word='FRA', categories={Tag.LANGUAGE}),
    ElementEntry(word='GER', categories={Tag.LANGUAGE}),
    ElementEntry(word='DEU', categories={Tag.LANGUAGE}),
    ElementEntry(word='ITA', categories={Tag.LANGUAGE}),
    ElementEntry(word='POR', categories={Tag.LANGUAGE}),
    ElementEntry(word='RUS', categories={Tag.LANGUAGE}),
    ElementEntry(word='ARA', categories={Tag.LANGUAGE}),
    ElementEntry(word='THA', categories={Tag.LANGUAGE}),
    ElementEntry(word='VIE', categories={Tag.LANGUAGE}),
    ElementEntry(word='POL', categories={Tag.LANGUAGE}),
    ElementEntry(word='DUT', categories={Tag.LANGUAGE}),
    ElementEntry(word='HUN', categories={Tag.LANGUAGE}),
    ElementEntry(word='TUR', categories={Tag.LANGUAGE}),
    ElementEntry(word='GRE', categories={Tag.LANGUAGE}),
    ElementEntry(word='HEB', categories={Tag.LANGUAGE}),
    ElementEntry(word='HIN', categories={Tag.LANGUAGE}),
    ElementEntry(word='SWE', categories={Tag.LANGUAGE}),
    ElementEntry(word='NOR', categories={Tag.LANGUAGE}),
    ElementEntry(word='UKR', categories={Tag.LANGUAGE}),
    ElementEntry(word='CZE', categories={Tag.LANGUAGE}),
    ElementEntry(word='RON', categories={Tag.LANGUAGE}),
    ElementEntry(word='FIN', categories={Tag.LANGUAGE}),
    ElementEntry(word='DAN', categories={Tag.LANGUAGE}),
    ElementEntry(word='PER', categories={Tag.LANGUAGE}),

    # Full names that commonly appear in anime filenames
    ElementEntry(word='ENGLISH', categories={Tag.LANGUAGE}),
    ElementEntry(word='JAPANESE', categories={Tag.LANGUAGE}),
    ElementEntry(word='CHINESE', categories={Tag.LANGUAGE}),
    ElementEntry(word='KOREAN', categories={Tag.LANGUAGE}),
    ElementEntry(word='SPANISH', categories={Tag.LANGUAGE}),
    ElementEntry(word='FRENCH', categories={Tag.LANGUAGE}),
    ElementEntry(word='GERMAN', categories={Tag.LANGUAGE}),
    ElementEntry(word='ITALIAN', categories={Tag.LANGUAGE}),
    ElementEntry(word='PORTUGUESE', categories={Tag.LANGUAGE}),
    ElementEntry(word='RUSSIAN', categories={Tag.LANGUAGE}),

    # Two-letter codes only when unambiguous (no conflicts with other tokens)
    ElementEntry(word='EN', categories={Tag.LANGUAGE}),
    ElementEntry(word='JP', categories={Tag.LANGUAGE}),
    ElementEntry(word='SP', categories={Tag.LANGUAGE}),
    ElementEntry(word='CH', categories={Tag.LANGUAGE}),
    ElementEntry(word='FR', categories={Tag.LANGUAGE}),
    ElementEntry(word='DE', categories={Tag.LANGUAGE}),
    ElementEntry(word='RU', categories={Tag.LANGUAGE}),
    ElementEntry(word='PL', categories={Tag.LANGUAGE}),
    ElementEntry(word='NL', categories={Tag.LANGUAGE}),
    ElementEntry(word='PT', categories={Tag.LANGUAGE}, regex_dict={
        r'PT[\W_]?BR': {0: {Tag.LANGUAGE}}
    }),

    # Common shorthands specific to anime releases
    ElementEntry(word='VOSTFR', categories={Tag.LANGUAGE}),  # French sub
    ElementEntry(word='PTBR', categories={Tag.LANGUAGE}),  # Brazilian Portuguese
    ElementEntry(word='ESP', categories={Tag.LANGUAGE}),  # Spanish alt
    ElementEntry(word='DEUTSCH', categories={Tag.LANGUAGE}),  # German alt

    # Chinese variants (important for anime — lots of sub groups)
    ElementEntry(word='ZH', categories={Tag.LANGUAGE}),
    ElementEntry(word='SC', categories={Tag.LANGUAGE}),  # Simplified Chinese
    ElementEntry(word='TC', categories={Tag.LANGUAGE}),  # Traditional Chinese
    ElementEntry(word='CHS', categories={Tag.LANGUAGE}),
    ElementEntry(word='CHT', categories={Tag.LANGUAGE}),
    ElementEntry(word='GB', categories={Tag.LANGUAGE}),
    ElementEntry(word='MANDARIN', categories={Tag.LANGUAGE}),
    ElementEntry(word='CANTONESE', categories={Tag.LANGUAGE}),
    # Note: TAIWANESE intentionally excluded — it's a modifier (e.g., "Taiwanese Mandarin")
    # not a standalone language identifier

    # Indonesian / Malay (common in SEA anime community)
    ElementEntry(word='IND', categories={Tag.LANGUAGE}),
    ElementEntry(word='MAL', categories={Tag.LANGUAGE}),

    # CJK language/dub descriptors
    ElementEntry(word='中文配', categories={Tag.LANGUAGE}),   # Chinese dub
    ElementEntry(word='中文配音', categories={Tag.LANGUAGE}),  # Chinese dub (full)
    ElementEntry(word='台粤配', categories={Tag.LANGUAGE}),   # Taiwanese+Cantonese dub
    ElementEntry(word='国语', categories={Tag.LANGUAGE}),    # Mandarin
    ElementEntry(word='國語', categories={Tag.LANGUAGE}),    # Mandarin (traditional)
    ElementEntry(word='粤语', categories={Tag.LANGUAGE}),    # Cantonese
    ElementEntry(word='粵語', categories={Tag.LANGUAGE}),    # Cantonese (traditional)
    ElementEntry(word='中配版', categories={Tag.LANGUAGE}),   # Chinese dub version
    ElementEntry(word='中配', categories={Tag.LANGUAGE}),    # Chinese dub (short)
    ElementEntry(word='国语版', categories={Tag.LANGUAGE}),   # Mandarin version
    ElementEntry(word='國語版', categories={Tag.LANGUAGE}),   # Mandarin version (traditional)
]
