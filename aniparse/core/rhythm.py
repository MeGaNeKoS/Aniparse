from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from aniparse.core import constant

if TYPE_CHECKING:
    from aniparse.core.token import Tokens


@dataclass
class BracketGroup:
    """Represents a bracket group with its positional metadata."""
    group_index: int          # 0-based index among all bracket groups
    open_pos: int             # token list index of the open bracket
    close_pos: int            # token list index of the close bracket
    is_first: bool = False    # is this the first bracket group?
    is_last: bool = False     # is this the last bracket group?
    starts_filename: bool = False  # does it start at position 0?


@dataclass
class DelimiterProfile:
    primary: str | None = None
    counts: dict[str, int] = field(default_factory=dict)
    is_uniform: bool = False
    file_index_end: int | None = None
    bracket_groups: list[BracketGroup] = field(default_factory=list)


def analyze_delimiters(tokens: Tokens) -> DelimiterProfile:
    """Analyze delimiter patterns across all tokens outside brackets."""
    profile = DelimiterProfile()
    counts: dict[str, int] = {}
    in_bracket = 0

    for token in tokens:
        if token.content in constant.OPEN_BRACKETS:
            in_bracket += 1
            continue
        if token.content in constant.CLOSE_BRACKETS:
            in_bracket = max(0, in_bracket - 1)
            continue
        if in_bracket > 0:
            continue

        if len(token.content) == 1 and token.content in constant.DELIMITERS:
            c = token.content
            counts[c] = counts.get(c, 0) + 1

    profile.counts = counts
    if not counts:
        return profile

    profile.primary = max(counts, key=counts.get)
    unique_types = set(counts.keys())
    profile.is_uniform = len(unique_types) == 1

    _detect_file_index(tokens, profile)
    _detect_bracket_groups(tokens, profile)

    return profile


def _detect_file_index(tokens: Tokens, profile: DelimiterProfile):
    """Detect leading number + delimiter file index pattern like '01. title here'."""
    token_list = tokens.tokens
    if len(token_list) < 3:
        return

    first = token_list[0]
    second = token_list[1]

    if not first.content.isdigit():
        return
    if len(second.content) != 1 or second.content not in constant.DELIMITERS:
        return

    sep = second.content
    rest_counts = dict(profile.counts)
    rest_counts[sep] = rest_counts.get(sep, 1) - 1
    if rest_counts[sep] <= 0:
        del rest_counts[sep]

    if rest_counts:
        rest_primary = max(rest_counts, key=rest_counts.get)
        if sep != rest_primary:
            profile.file_index_end = 2


def _detect_bracket_groups(tokens: Tokens, profile: DelimiterProfile):
    """Detect bracket groups and annotate tokens with their bracket group info."""
    token_list = tokens.tokens
    groups = []
    i = 0
    while i < len(token_list):
        t = token_list[i]
        if t.content in constant.OPEN_BRACKETS:
            # Find matching close bracket of same type
            expected_close = constant.BRACKET_PAIRS.get(t.content)
            for j in range(i + 1, len(token_list)):
                if token_list[j].content == expected_close:
                    bg = BracketGroup(
                        group_index=len(groups),
                        open_pos=i,
                        close_pos=j,
                    )
                    groups.append(bg)
                    # Annotate interior tokens
                    for k in range(i + 1, j):
                        token_list[k].bracket_group = bg
                    i = j + 1
                    break
            else:
                i += 1
        else:
            i += 1

    if groups:
        groups[0].is_first = True
        groups[-1].is_last = True
        groups[0].starts_filename = (groups[0].open_pos == 0)

    profile.bracket_groups = groups
