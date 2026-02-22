from __future__ import annotations

import logging
import re
import warnings
from typing import List

from aniparse.config import ParserConfig
from aniparse.wordlist import WordListManager
from aniparse.abstraction.keyword_base import ElementEntry
from aniparse.abstraction.parser_base import AbstractParser, Possibilities
from aniparse.abstraction.score_base import Score
from aniparse.core.compose import compose
from aniparse.core.resolve import resolve, calculate_confidence
from aniparse.core.rhythm import analyze_delimiters
from aniparse.core.token import Tokens, Token
from aniparse.core.tokenizer import Tokenizer

logger = logging.getLogger(__name__)


def _both_have_regex(p_entries, s_entries):
    """Return True if both sides have at least one entry with regex patterns."""
    return (any(e.regex_dict for e in p_entries)
            and any(e.regex_dict for e in s_entries))


class BaseParser(AbstractParser):
    def __init__(self,
                 filename: str,
                 word_list_manager: WordListManager,
                 possibilities: Possibilities = None,
                 score: Score = None,
                 config: ParserConfig = None):
        self.tokens: Tokens = Tokenizer(filename, word_list_manager).tokenize()
        self._filename = filename
        self.word_list_manager = word_list_manager
        self.config = config or ParserConfig()

        self.possibilities = possibilities or Possibilities()
        self.warn = []

        if score is None:
            self.score: Score = Score()
        else:
            self.score: Score = score

        self.delimiter_profile = analyze_delimiters(self.tokens)
        self.processed_entries = set()

    @staticmethod
    def get_entry_id(token: Token, entry: ElementEntry):
        return f"{id(token)}_{id(entry)}"

    def process_entry(self, word: str, tokens: list[Token], entry: ElementEntry):
        """Process a single entry for a word."""
        entry_id = self.get_entry_id(tokens[0], entry)
        self.add_possibility(tokens, entry)
        if entry_id in self.processed_entries:
            return
        self.processed_entries.add(entry_id)
        self.process_regex_matches(tokens[-1], entry)

    @staticmethod
    def add_possibility(tokens: list[Token], entry: ElementEntry):
        """Process category sets of an entry."""
        for category_set in entry.categories:
            for token in tokens:
                token.add_possibility(category_set, element=entry)

    def process_regex_matches(self, token: Token, entry: ElementEntry):
        """Process regex matches for a word."""
        for regex, group_possibilities in entry.regex_dict.items():
            with warnings.catch_warnings(record=True) as warn:
                for match in re.finditer(regex, self.filename, re.IGNORECASE):
                    if match.start() <= token.index < match.end():
                        for group_idx, possibilities in group_possibilities.items():
                            matched_group_start, matched_group_end = match.span(group_idx)
                            matched_tokens = self.get_matched_tokens_range(matched_group_start, matched_group_end)
                            for target_token in matched_tokens:
                                target_token.add_possibility(possibilities, element=entry, base_score=1.5)
                if warn and any(issubclass(item.category, FutureWarning) for item in warn):
                    logger.warning(f'Warning from "{entry.word}", regex: "{regex}"')
                    self.warn.append((f'Warning from "{entry.word}", regex: "{regex}"', warn))

    def get_matched_tokens_range(self, start: int, end: int) -> List[Token]:
        """Get tokens matched by the regex within a specific range."""
        matched_tokens = []
        for token in self.tokens:
            if start <= token.index < end:
                matched_tokens.append(token)
        return matched_tokens


class ParserProcessor(BaseParser):
    def assign_possibilities(self):
        fuzzy = self.config.fuzzy
        threshold = self.config.fuzzy_threshold
        for token in self.tokens:
            for entry in self.word_list_manager.find(token.content, fuzzy=fuzzy, threshold=threshold):
                self.process_entry(token.content, [token], entry)

        self._resplit_compound_tokens()
        self.possibilities.apply_all(self)

    def _resplit_compound_tokens(self):
        """Split unmatched tokens into sub-tokens that match known keywords."""
        token_list = self.tokens.tokens
        i = 0
        while i < len(token_list):
            token = token_list[i]
            if token.possibilities or len(token.content) < 2 or not token.bracket_group:
                i += 1
                continue
            split = self._find_keyword_split(token.content)
            if split:
                sp, prefix, suffix, p_entries, s_entries = split
                t1 = Token(content=prefix, index=token.index)
                t2 = Token(content=suffix, index=token.index + sp)
                t1.bracket_group = token.bracket_group
                t2.bracket_group = token.bracket_group
                t1.zone = token.zone
                t2.zone = token.zone
                # Replace in token list and register with Tokens container
                token.remove_observer(self.tokens)
                token_list[i:i + 1] = [t1, t2]
                t1.add_observer(self.tokens)
                t2.add_observer(self.tokens)
                self.tokens.lookup_category.setdefault(t1.category, []).append(t1)
                self.tokens.lookup_category.setdefault(t2.category, []).append(t2)
                # Remove old token from lookup
                if token in self.tokens.lookup_category.get(token.category, []):
                    self.tokens.lookup_category[token.category].remove(token)
                t2.split_boundary = True  # mark for compose group-breaking
                for entry in p_entries:
                    self.process_entry(prefix, [t1], entry)
                for entry in s_entries:
                    self.process_entry(suffix, [t2], entry)
                i += 2
            else:
                i += 1

    def _find_keyword_split(self, content):
        """Find a split point where both sides match known keywords.

        Requires both halves to be at least 2 chars, unless both match keywords.
        """
        # First pass: both sides >= 2 chars
        for sp in range(2, len(content) - 1):
            prefix, suffix = content[:sp], content[sp:]
            p_entries = list(self.word_list_manager.find(prefix))
            s_entries = list(self.word_list_manager.find(suffix))
            if p_entries and s_entries and _both_have_regex(p_entries, s_entries):
                return (sp, prefix, suffix, p_entries, s_entries)
        # Second pass: allow 1-char halves only when both match and content >= 4 chars
        if len(content) >= 4:
            for sp in (1, len(content) - 1):
                prefix, suffix = content[:sp], content[sp:]
                p_entries = list(self.word_list_manager.find(prefix))
                s_entries = list(self.word_list_manager.find(suffix))
                if p_entries and s_entries and _both_have_regex(p_entries, s_entries):
                    return (sp, prefix, suffix, p_entries, s_entries)
        return None

    def score_token_possibilities(self):
        for token in self.tokens:
            if not token.possibilities:
                continue
            for label in list(token.possibilities.keys()):
                self.score.calculate(label, token, self.tokens)


class Parser(ParserProcessor):
    def parse(self, debug: bool = False) -> dict | None:
        if not self.tokens:
            return None

        self.assign_possibilities()
        self.score_token_possibilities()

        resolve(self.tokens)
        confidence = calculate_confidence(self.tokens)
        metadata = compose(self.tokens, self._filename, self.delimiter_profile, self.config)

        result = metadata.to_dict()

        result["_confidence"] = round(confidence, 4)

        if debug:
            result["_debug"] = {
                "tokens": [
                    {
                        "content": t.content,
                        "category": t.category.value,
                        "possibilities": {
                            label.value: {"descriptor": p.descriptor.value, "score": p.score}
                            for label, p in t.possibilities.items()
                        },
                    }
                    for t in self.tokens
                ]
            }

        return result
