"""User-configurable parser settings.

These defaults are language-dependent and can be overridden per Aniparse instance.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ParserConfig:
    """Configuration for locale-dependent parsing behaviour."""

    year_min: int = 1900
    year_max: int = 2099

    range_total: set[str] = field(default_factory=lambda: {"of"})
    range_separator: set[str] = field(default_factory=lambda: {"-", "~", "&", "+"})
    range_connectors: set[str] = field(default_factory=lambda: {"&", "+"})

    fuzzy: bool = False
    fuzzy_threshold: float = 0.8

    ordinal_suffixes: tuple[str, ...] = ('st', 'nd', 'rd', 'th')

    ordinals: dict[str, str] = field(default_factory=lambda: {
        'first': '1',
        'second': '2',
        'third': '3',
        'fourth': '4',
        'fifth': '5',
        'sixth': '6',
        'seventh': '7',
        'eighth': '8',
        'ninth': '9',
    })
