from __future__ import annotations

from aniparse.core import constant
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag


class BracketContentPossibilityRule(PossibilityRule):
    """Scan all bracket groups and tag unknown content as release group candidates."""

    @classmethod
    def apply(cls, parser: AbstractParser):
        tokens = parser.tokens
        token_list = list(tokens)

        bracket_groups = []
        i = 0
        while i < len(token_list):
            token = token_list[i]
            if Tag.BRACKET in token.possibilities and token.content in constant.OPEN_BRACKETS:
                inside = []
                close_idx = None
                expected_close = constant.BRACKET_PAIRS.get(token.content)
                for j in range(i + 1, len(token_list)):
                    t = token_list[j]
                    if Tag.BRACKET in t.possibilities and t.content == expected_close:
                        close_idx = j
                        break
                    inside.append(t)
                if close_idx is not None:
                    bracket_groups.append((i, inside, close_idx))
                    i = close_idx + 1
                    continue
            i += 1

        for group_idx, (open_pos, inside_tokens, close_pos) in enumerate(bracket_groups):
            if not inside_tokens:
                continue

            # Skip first bracket at position 0 — handled by ReleaseGroupRule
            if open_pos == 0:
                continue

            # Check if all non-delimiter tokens are unknown
            has_metadata = False
            has_unknown = False
            for t in inside_tokens:
                non_structural = {k for k in t.possibilities
                                  if k not in (Tag.DELIMITER, Tag.CONTEXT_DELIMITER, Tag.BRACKET)}
                if not non_structural and not t.possibilities:
                    has_unknown = True
                elif non_structural:
                    metadata_labels = Tag.get_optional_info()
                    if any(k in metadata_labels for k in non_structural):
                        has_metadata = True
                    else:
                        has_unknown = True

            if has_unknown and not has_metadata:
                first_at_zero = bracket_groups[0][0] == 0
                is_last = (group_idx == len(bracket_groups) - 1)
                # Skip release group tagging if first bracket already serves as release group
                if first_at_zero:
                    continue
                score = 1.0 if is_last else 0.5
                for t in inside_tokens:
                    if not t.possibilities or Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                        t.add_possibility(Tag.RELEASE_GROUP, base_score=score)
