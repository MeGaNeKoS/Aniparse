from __future__ import annotations

from aniparse.core import constant
from aniparse.core.constant import BASE_METADATA_LABELS
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag


class ReleaseGroupPossibilityRule(PossibilityRule):
    """Identify release group from the first and last bracket groups, plus trailing unbracketed."""

    METADATA_LABELS = BASE_METADATA_LABELS | {
        Tag.SEQUENCE_PREFIX, Tag.SEQUENCE_NUMBER,
        Tag.FILE_INDEX, Tag.YEAR, Tag.TYPE,
    }

    @staticmethod
    def _is_metadata_bracket(inside_tokens, strong_labels):
        """Return True if all non-delimiter tokens have only strong metadata possibilities."""
        for t in inside_tokens:
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                continue
            if not t.possibilities:
                return False  # unknown token = not pure metadata
            if not (t.possibilities.keys() <= strong_labels):
                return False
        return True

    @classmethod
    def _check_trailing_release_group(cls, token_list):
        """Check for trailing unbracketed release group like '-dhd' or '-ank' at end."""
        # Walk backwards from end, skip extension-like tokens
        end = len(token_list) - 1
        # Skip file extension (last unknown after dot delimiter) — only if it looks like an extension (2-4 chars)
        last_tok = token_list[end]
        if (end >= 2 and not last_tok.possibilities
                and len(last_tok.content) <= 4
                and Tag.DELIMITER in token_list[end - 1].possibilities
                and token_list[end - 1].content == constant.DOT
                and last_tok.content.lower() in constant.FILE_EXTENSIONS):
            end -= 2

        # Collect trailing UNKNOWN tokens (the group name)
        trailing = []
        i = end
        while i >= 0:
            t = token_list[i]
            if not t.possibilities:
                trailing.append(t)
                i -= 1
            elif Tag.DELIMITER in t.possibilities and t.content.strip():
                trailing.append(t)
                i -= 1
            else:
                break


        if not trailing:
            return

        if i < 0:
            return

        # The token at position i is the first non-trailing token (metadata or delimiter)
        # Find the last real metadata token before trailing
        last_meta_idx = None
        last_meta_is_pure_sequence = False
        for k in range(i, -1, -1):
            pk = token_list[k].possibilities.keys()
            if Tag.DELIMITER in pk or Tag.CONTEXT_DELIMITER in pk:
                continue
            if not pk or Tag.TITLE in pk:
                continue
            # Found a metadata token
            sequence_like = {Tag.SEQUENCE_NUMBER, Tag.FILE_INDEX, Tag.YEAR}
            if pk <= sequence_like:
                last_meta_is_pure_sequence = True
            else:
                last_meta_idx = k
            break

        # Only tag as release group if preceded by real metadata (not just episode number)

        if last_meta_idx is not None and not last_meta_is_pure_sequence:
            for t in trailing:
                if not t.possibilities:
                    t.add_possibility(Tag.RELEASE_GROUP, base_score=0.7)

    @classmethod
    def _check_comma_separated_release_group(cls, bracket_groups, strong_metadata):
        """Detect release group in delimiter-separated bracket: '(group, 720p)' or '[hqr.remux]'."""
        for _, inside, _ in bracket_groups:
            if not inside:
                continue
            # Split inside tokens by comma or dot
            sections = []
            current = []
            for t in inside:
                if Tag.DELIMITER in t.possibilities and t.content.strip() and t.content != constant.UNDERSCORE:
                    if current:
                        sections.append(current)
                    current = []
                else:
                    current.append(t)
            if current:
                sections.append(current)
            if len(sections) < 2:
                continue
            # Check each section: is it all unknown or all metadata?
            unknown_sections = []
            has_metadata_section = False
            for section in sections:
                words = [t for t in section
                         if Tag.DELIMITER not in t.possibilities]
                if not words:
                    continue
                all_unknown = all(not t.possibilities for t in words)
                all_meta = all(
                    t.possibilities and t.possibilities.keys() <= (strong_metadata | {Tag.DELIMITER, Tag.CONTEXT_DELIMITER, Tag.SEQUENCE_PART})
                    for t in words
                )
                if all_unknown:
                    unknown_sections.append(section)
                elif all_meta:
                    has_metadata_section = True
            # If we have at least one unknown section AND at least one metadata section,
            # tag the unknown section as release group
            if unknown_sections and has_metadata_section:
                for section in unknown_sections:
                    for t in section:
                        if not t.possibilities or Tag.DELIMITER in t.possibilities:
                            t.add_possibility(Tag.RELEASE_GROUP, base_score=0.8)
                return  # only tag one bracket

    @classmethod
    def _check_trailing_release_group_after_brackets(cls, token_list):
        """Detect trailing release group after the last bracket: ']_-_thora'."""
        end = len(token_list) - 1

        # Skip trailing version-like tokens (e.g., "v2" → CONTEXT_DELIMITER + SEQUENCE_NUMBER)
        i = end
        while i >= 0:
            t = token_list[i]
            pk = t.possibilities.keys()
            if Tag.RELEASE_VERSION in pk:
                i -= 1
                continue
            # Skip version context delimiter (e.g., "v" before version number) and its number
            if Tag.CONTEXT_DELIMITER in pk and Tag.RELEASE_VERSION not in pk:
                i -= 1
                continue
            if Tag.SEQUENCE_NUMBER in pk and Tag.DELIMITER not in pk and not t.possibilities.keys() - {Tag.SEQUENCE_NUMBER, Tag.FILE_INDEX}:
                # Number after version context delimiter — check if preceded by one
                if i > 0 and Tag.CONTEXT_DELIMITER in token_list[i - 1].possibilities:
                    i -= 1
                    continue
            if Tag.DELIMITER in pk and not t.content.strip():
                i -= 1
                continue
            break

        # Collect trailing unknown tokens
        trailing = []
        while i >= 0:
            t = token_list[i]
            if not t.possibilities:
                trailing.append(t)
                i -= 1
            elif Tag.DELIMITER in t.possibilities and t.content.strip():
                trailing.append(t)
                i -= 1
            else:
                break

        if not trailing or i < 0:
            return

        # Now expect: optional delimiters/dashes, then a closing bracket
        j = i
        found_close_bracket = False
        while j >= 0:
            t = token_list[j]
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                j -= 1
                continue
            if Tag.BRACKET in t.possibilities and t.content in constant.CLOSE_BRACKETS:
                found_close_bracket = True
            break

        if found_close_bracket:
            for t in trailing:
                if not t.possibilities:
                    t.add_possibility(Tag.RELEASE_GROUP, base_score=0.8)

    @classmethod
    def apply(cls, parser: AbstractParser):

        tokens = parser.tokens
        token_list = list(tokens)

        # Handle broken bracket pattern: ]text] at start of filename
        # (missing opening [ — treat as release group)
        if (len(token_list) >= 3
                and Tag.BRACKET in token_list[0].possibilities
                and token_list[0].content in constant.CLOSE_BRACKETS):
            # Find the next close bracket to close this broken bracket
            for j in range(1, len(token_list)):
                t = token_list[j]
                if Tag.BRACKET in t.possibilities and t.content in constant.CLOSE_BRACKETS:
                    # Tag everything between as release group
                    for k in range(1, j):
                        token_list[k].add_possibility(Tag.RELEASE_GROUP, base_score=1.5)
                    break
                if t.category == Tag.DELIMITER and t.content.strip() == '':
                    break  # space before close ] means it's not a bracket group

        # Find all bracket groups
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


        if not bracket_groups:
            # Still check for trailing release group in bracketless filenames

            cls._check_trailing_release_group(token_list)
            return

        # Process leading bracket groups and last bracket
        STRONG_METADATA = BASE_METADATA_LABELS | {
            Tag.SEQUENCE_NUMBER, Tag.YEAR, Tag.FILE_CHECKSUM,
            Tag.RELEASE_INFORMATION, Tag.FILE_INDEX,
        }
        candidates = []
        first_open_pos, first_inside, _ = bracket_groups[0]
        # Treat first bracket as release group if at position 0,
        # or preceded by only a single word + dot (e.g., "evobot.[group]")
        first_bracket_is_rg = first_open_pos == 0 and first_inside
        if not first_bracket_is_rg and first_inside and first_open_pos > 0:
            pre_tokens = token_list[:first_open_pos]
            # Single word + dot before bracket (no spaces)
            if (len(pre_tokens) == 2
                    and not pre_tokens[0].possibilities
                    and Tag.DELIMITER in pre_tokens[1].possibilities
                    and pre_tokens[1].content.strip()):
                first_bracket_is_rg = True
        if first_bracket_is_rg:
            candidates.append((first_inside, 1.5))
            # Check for consecutive brackets immediately after the first
            # (e.g., [group1][group2][group3]_title...)
            for bg_idx in range(1, len(bracket_groups)):
                bg_open_pos, bg_inside, _ = bracket_groups[bg_idx]
                prev_close_idx = bracket_groups[bg_idx - 1][2]
                # Check if only delimiters between previous close bracket and this open bracket
                all_delim = True
                for j in range(prev_close_idx + 1, bg_open_pos):
                    t = token_list[j]
                    if Tag.DELIMITER not in t.possibilities:
                        all_delim = False
                        break
                if all_delim and bg_inside and not cls._is_metadata_bracket(bg_inside, STRONG_METADATA):
                    # Skip long bracket groups (>4 words) — these are likely titles, not release groups
                    word_count = sum(1 for t in bg_inside
                                     if Tag.DELIMITER not in t.possibilities
                                     and Tag.CONTEXT_DELIMITER not in t.possibilities)
                    if word_count <= 4:
                        candidates.append((bg_inside, 1.3))
                else:
                    break

        # Last bracket: only if no first-bracket release group candidate
        has_first_bracket_rg = first_open_pos == 0 and first_inside
        if len(bracket_groups) > 1 and not has_first_bracket_rg:
            for idx in range(len(bracket_groups) - 1, 0, -1):
                _, inside, _ = bracket_groups[idx]
                if inside and not cls._is_metadata_bracket(inside, STRONG_METADATA):
                    candidates.append((inside, 1.0))
                    break

        for inside_tokens, score in candidates:
            if score == 1.5:
                # First bracket at position 0: tag all content as release group candidate
                # Positional scoring will boost this further
                for token in inside_tokens:
                    token.add_possibility(Tag.RELEASE_GROUP, base_score=1.5)
            else:
                # Last bracket: only tag if contains unknown tokens without metadata
                has_unknown = any(not t.possibilities for t in inside_tokens)
                # Check for strong metadata (not just language — groups can contain language codes)
                WEAK_LABELS = {Tag.DELIMITER, Tag.CONTEXT_DELIMITER, Tag.LANGUAGE, Tag.CONTEXT_DEPENDENT,
                              Tag.SEQUENCE_NUMBER, Tag.FILE_INDEX, Tag.SUBS_TERM}
                has_strong_metadata = any(
                    t.possibilities and not (t.possibilities.keys() <= WEAK_LABELS)
                    for t in inside_tokens
                )
                if has_unknown and not has_strong_metadata:
                    for token in inside_tokens:
                        token.add_possibility(Tag.RELEASE_GROUP, base_score=score)

        # Check for comma-separated mixed brackets: "(group name, 720p)"
        # Tag the unknown section as RELEASE_GROUP
        cls._check_comma_separated_release_group(bracket_groups, STRONG_METADATA)

        # Trailing unbracketed release group after last bracket: "-GroupName" at end
        # Only if preceded by a closing bracket (with delimiters between)
        cls._check_trailing_release_group_after_brackets(token_list)
