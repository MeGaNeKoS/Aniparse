from __future__ import annotations

import logging
import re
import warnings
from typing import List, Type

from aniparse import WordListManager
from aniparse.abstraction.ParserBase import AbstractParser, PossibilityRule
from aniparse.abstraction.ScoreBase import Score
from aniparse.token import Tokens, Token
from aniparse.tokenizer import Tokenizer

logger = logging.getLogger(__name__)


class BaseParser(AbstractParser):
    def __init__(self,
                 filename: str,
                 word_list_manager: WordListManager,
                 possibility_rule: List[Type[PossibilityRule]] = None,
                 score: Score = None):
        self.tokens: Tokens = Tokenizer(filename).tokenize()
        self._filename = filename
        self.word_list_manager = word_list_manager

        self.possibility_rule: List[Type[PossibilityRule]] = possibility_rule or []

        if score is None:
            self.score: Score = Score()
        else:
            self.score: Score = score

        self.processed_entries = set()

    @staticmethod
    def get_entry_id(word, entry):
        # Create a unique identifier for each entry, for example:
        return f"{word}_{id(entry)}"

    def process_entry(self, word, tokens, entry):
        """Process a single entry for a word."""

        entry_id = self.get_entry_id(word, entry)
        self.process_categories(tokens, entry)
        if entry_id in self.processed_entries:
            return
        self.processed_entries.add(entry_id)

        self.process_regex_matches(tokens[-1], entry)
        self.process_continuations(word, tokens, entry)

    def process_categories(self, tokens, entry):
        """Process category sets of an entry."""
        for category_set in entry.category_set:
            for token in tokens:
                token.add_possibility(category_set)

    def process_regex_matches(self, token, entry):
        """Process regex matches for a word."""
        for regex, group_possibilities in entry.regex_dict.items():
            with warnings.catch_warnings(record=True) as w:
                for match in re.finditer(regex, self.filename, re.IGNORECASE):
                    if match.start() <= token.index < match.end():
                        for group_idx, possibilities in group_possibilities.items():
                            matched_group_start, matched_group_end = match.span(group_idx)
                            matched_tokens = self.get_matched_tokens_range(matched_group_start, matched_group_end)
                            for target_token in matched_tokens:
                                target_token.add_possibility(possibilities)
                if w and any(issubclass(item.category, FutureWarning) for item in w):
                    logger.warning(f'Warning from "{entry.word}", regex: "{regex}"')

    def get_matched_tokens_range(self, start, end) -> List[Token]:
        """Get tokens matched by the regex within a specific range."""
        matched_tokens = []

        for token in self.tokens:
            if start <= token.index < end:
                matched_tokens.append(token)

        return matched_tokens

    def process_continuations(self, word, tokens, entry):
        """Process continuations of an entry for a word."""
        for continuation in entry.continuation_set:
            next_token = self.tokens.find_next(tokens[-1])
            if next_token and next_token.content.upper() == continuation.upper():
                combined_word = word + next_token.content
                tokens.append(next_token)
                for continuation_entry in self.word_list_manager.exists(combined_word):
                    self.process_entry(combined_word, tokens, continuation_entry)


class ParserProcessor(BaseParser):
    def assign_possibilities(self):
        for token in self.tokens:
            # This part already correct, No need to check this
            for entry in self.word_list_manager.exists(token.content):
                # token.token_entries.add(entry)
                self.process_entry(token.content, [token], entry)

        for rule in self.possibility_rule:
            rule.apply(self)

    def score_token_possibilities(self):
        for token in self.tokens:
            if not token.possibilities:
                continue

            for possibilities in token.possibilities:
                self.score.calculate(possibilities, token, self.tokens)


class Parser(ParserProcessor):
    def parse(self):
        if not self.tokens:
            return None

        self.assign_possibilities()
        # self.score_token_possibilities()
