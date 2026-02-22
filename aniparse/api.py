"""Public API: Aniparse class (configurable) and parse() convenience wrapper."""
from __future__ import annotations

import os
import re

from aniparse import keyword
from aniparse.config import ParserConfig
from aniparse.core import constant
from aniparse.core.constant import DEFAULT_PROVIDER_NAME
from aniparse.core.defaults import build_default_score, build_default_possibilities
from aniparse.core.parser import Parser
from aniparse.wordlist import InMemoryWordListProvider, WordListManager


def _split_on_pipe(filename: str) -> list[str]:
    """Split filename on | but not when inside brackets/parens."""
    segments = []
    current = []
    depth = 0
    for ch in filename:
        if ch in constant.OPEN_BRACKETS:
            depth += 1
        elif ch in constant.CLOSE_BRACKETS:
            depth = max(0, depth - 1)
        if ch == constant.PIPE and depth == 0:
            segments.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    segments.append(''.join(current).strip())
    return segments


def _build_default_wordlist() -> WordListManager:
    provider = InMemoryWordListProvider()
    manager = WordListManager()
    manager.add_provider(DEFAULT_PROVIDER_NAME, provider)
    for word in keyword.DEFAULT_KEYWORD:
        provider.add_word(word)
    return manager


def _parse_folder_segment(segment: str, wlm, config) -> dict | None:
    """Parse a single folder segment and return its result dict."""
    segment = segment.strip()
    if not segment:
        return None
    parser = Parser(
        filename=segment,
        word_list_manager=wlm,
        possibilities=build_default_possibilities(),
        score=build_default_score(),
        config=config,
    )
    return parser.parse(debug=False)


def _reinterpret_folder_result(result: dict) -> dict:
    """Reinterpret folder parse results: bare episodes become seasons."""
    if not result or not result.get("series"):
        return result
    series = result["series"][0]
    # A folder with only episode(s) and no title/season/type → treat as season
    has_title = "title" in series
    has_season = "season" in series
    has_type = "type" in series
    has_episode = "episode" in series
    if has_episode and not has_title and not has_season and not has_type:
        series["season"] = series.pop("episode")
    return result


def _merge_folder_context(result: dict, folder: str, wlm, config):
    """Parse folder segments and gap-fill into the filename result."""
    segments = re.split(r'[/\\]', folder)
    segments = [s for s in segments if s.strip()]
    if not segments:
        return

    # Parse each segment outermost-first, layer into combined context
    # Inner segments override outer for same series-level fields
    combined_series = {}
    _SERIES_FIELDS = ("title", "season", "year", "type")

    for seg in segments:
        seg_result = _parse_folder_segment(seg, wlm, config)
        if not seg_result:
            continue
        seg_result = _reinterpret_folder_result(seg_result)
        if seg_result.get("series"):
            seg_series = seg_result["series"][0]
            for field in _SERIES_FIELDS:
                if field in seg_series:
                    combined_series[field] = seg_series[field]

    if not combined_series:
        return

    # Gap-fill into result's series[0]
    result.setdefault("series", [{}])
    file_series = result["series"][0]
    for field in _SERIES_FIELDS:
        if field in combined_series and field not in file_series:
            file_series[field] = combined_series[field]

    result["folder_name"] = folder


class Aniparse:
    """Configurable anime filename parser.

    Example::

        # Custom instance
        parser = Aniparse(wordlist_provider=my_wlm)
        result = parser.parse("[Group] Title - 01 [1080p].mkv")

        # Or just use the module-level convenience function
        import aniparse
        result = aniparse.parse("[Group] Title - 01 [1080p].mkv")
    """

    def __init__(self, wordlist_provider: WordListManager = None,
                 config: ParserConfig = None):
        self._wlm = wordlist_provider or _build_default_wordlist()
        self._config = config or ParserConfig()

    def parse(self, filename: str, *, folder: str = None, path: str = None,
              debug: bool = False) -> dict | None:
        """Parse an anime filename and return structured metadata.

        Args:
            filename: The filename to parse.
            folder: Optional folder name for context.
            path: If provided, splits into folder + filename automatically.
            debug: If True, include token scoring breakdown in output.

        Returns:
            Metadata dict matching the output.ts schema, or None if empty.
        """
        if path and not folder:
            folder = os.path.dirname(path)
            filename = os.path.basename(path) if not filename else filename

        score = build_default_score()
        possibilities = build_default_possibilities()

        # Split on | for alternative titles
        segments = [s.strip() for s in filename.split(constant.PIPE)]
        primary = segments[0]
        alternatives = segments[1:] if len(segments) > 1 else []

        # Strip trailing unclosed parenthesis from primary when it resulted from
        # splitting on | inside parens (e.g., "(TRIGUN STARGAZE | Season 2 | S2)")
        _open_paren = constant.OPEN_PARENS[0]  # ASCII '('
        _close_paren = constant.BRACKET_PAIRS[_open_paren]
        if alternatives and primary.count(_open_paren) > primary.count(_close_paren):
            last_open = primary.rfind(_open_paren)
            trailing = primary[last_open + 1:].strip()
            # Only strip if the trailing content looks like a title (no common metadata keywords)
            trailing_words = set(trailing.lower().split())
            if trailing and not (trailing_words & constant.BASE_METADATA_INDICATORS):
                primary = primary[:last_open].strip()
                alternatives.insert(0, trailing)
        # Clean alternatives: strip unmatched closing brackets
        _close_chars = ''.join(constant.CLOSE_BRACKETS)
        alternatives = [a.rstrip(_close_chars).strip() for a in alternatives]

        parser = Parser(
            filename=primary,
            word_list_manager=self._wlm,
            possibilities=possibilities,
            score=score,
            config=self._config,
        )

        result = parser.parse(debug=debug)
        if result is None:
            return None

        result["file_name"] = filename

        if alternatives:
            for alt in alternatives:
                alt = alt.strip()
                if not alt:
                    continue
                alt_parser = Parser(
                    filename=alt,
                    word_list_manager=self._wlm,
                    possibilities=build_default_possibilities(),
                    score=build_default_score(),
                    config=self._config,
                )
                alt_result = alt_parser.parse(debug=False)
                if alt_result and alt_result.get("series"):
                    alt_series = alt_result["series"][0]
                    alt_entry = {}
                    if "title" in alt_series:
                        alt_entry["title"] = alt_series["title"]
                    if alt_entry:
                        result.setdefault("series", []).append(alt_entry)

        if folder:
            _merge_folder_context(result, folder, self._wlm, self._config)

        return result


# Lazy default instance
_default: Aniparse | None = None


def parse(filename: str, *, folder: str = None, path: str = None,
          wordlist_provider: WordListManager = None,
          debug: bool = False) -> dict | None:
    """Convenience wrapper using a default Aniparse instance.

    Args:
        filename: The filename to parse.
        folder: Optional folder name for context.
        path: If provided, splits into folder + filename automatically.
        wordlist_provider: Custom WordListManager. Uses default if None.
        debug: If True, include token scoring breakdown in output.

    Returns:
        Metadata dict matching the output.ts schema, or None if empty.
    """
    if wordlist_provider:
        return Aniparse(wordlist_provider=wordlist_provider).parse(
            filename, folder=folder, path=path, debug=debug
        )

    global _default
    if _default is None:
        _default = Aniparse()
    return _default.parse(filename, folder=folder, path=path, debug=debug)
