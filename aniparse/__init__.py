"""Aniparse — Anime filename parser."""
from aniparse.api import Aniparse, parse
from aniparse.config import ParserConfig
from aniparse.output_schemas import Metadata
from aniparse.wordlist import WordListManager

__all__ = ["parse", "Aniparse", "ParserConfig", "Metadata", "WordListManager"]
