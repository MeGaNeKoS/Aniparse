from __future__ import annotations

from aniparse.core import constant
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag


class YearPossibilityRule(PossibilityRule):
    """Boost SERIES_YEAR score for numbers alone inside parentheses."""

    @classmethod
    def apply(cls, parser: AbstractParser):
        tokens = parser.tokens
        token_list = list(tokens)

        for i, token in enumerate(token_list):
            if Tag.BRACKET not in token.possibilities:
                continue
            if token.content not in constant.OPEN_BRACKETS:
                continue

            # Collect tokens inside bracket until close
            inside_tokens = []
            close_idx = None
            expected_close = constant.BRACKET_PAIRS.get(token.content)
            for j in range(i + 1, len(token_list)):
                t = token_list[j]
                if Tag.BRACKET in t.possibilities and t.content == expected_close:
                    close_idx = j
                    break
                inside_tokens.append(t)

            if close_idx is None or not inside_tokens:
                continue

            # Check if there's exactly one non-delimiter token inside
            non_delim = [t for t in inside_tokens
                         if Tag.DELIMITER not in t.possibilities
                         and Tag.CONTEXT_DELIMITER not in t.possibilities]

            if len(non_delim) != 1:
                continue

            candidate = non_delim[0]
            if not candidate.content.isdigit():
                continue

            val = int(candidate.content)
            if parser.config.year_min <= val <= parser.config.year_max:
                candidate.add_possibility(Tag.SERIES_YEAR, base_score=2.0)
