from __future__ import annotations

from aniparse.core import constant
from aniparse.core.constant import BASE_METADATA_LABELS
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag

class TitlePossibilityRule(PossibilityRule):
    """Identify title tokens from consecutive UNKNOWN tokens outside brackets."""

    # Labels that indicate metadata (not title)
    METADATA_LABELS = BASE_METADATA_LABELS | {
        Tag.SEQUENCE_PREFIX,
        Tag.RELEASE_GROUP,
    }

    # SEQUENCE_NUMBER alone is not enough to stop title — needs structural evidence
    SEQUENCE_ONLY_LABELS = {Tag.SEQUENCE_NUMBER}

    # Labels that are ambiguous in title context (could be title words)
    AMBIGUOUS_IN_TITLE = {Tag.LANGUAGE, Tag.SUBS_TERM, Tag.RELEASE_INFORMATION, Tag.EXTRA_INFO}

    @classmethod
    def apply(cls, parser: AbstractParser):
        tokens = parser.tokens

        extension_token = cls._find_extension_token(tokens)

        bracket_depth = 0
        title_candidates = []
        found_metadata = False
        found_metadata_type = None  # track what kind of metadata stopped us

        token_list = tokens.tokens
        skip_until = -1
        for idx, token in enumerate(token_list):
            if idx <= skip_until:
                continue

            # Track bracket nesting via possibilities
            if Tag.BRACKET in token.possibilities:
                if token.content in constant.OPEN_BRACKETS:
                    # Check if bracket content should be part of title
                    if bracket_depth == 0 and not found_metadata and title_candidates:
                        bracket_tokens, end_idx = cls._get_title_bracket_content(
                            token_list, idx, cls.METADATA_LABELS | cls.SEQUENCE_ONLY_LABELS)
                        if bracket_tokens is not None:
                            title_candidates.extend(bracket_tokens)
                            skip_until = end_idx
                            continue
                        # Release group bracket before real title text:
                        # clear pre-bracket if unknown text follows after bracket
                        # (e.g., "evobot.[group]_real_title_here")
                        if (cls._bracket_has_release_group(token_list, idx)
                                and cls._has_unknown_after_bracket(token_list, idx)):
                            found_metadata = True
                            found_metadata_type = Tag.RELEASE_GROUP
                            title_candidates.clear()
                    bracket_depth += 1
                elif token.content in constant.CLOSE_BRACKETS:
                    bracket_depth = max(0, bracket_depth - 1)
                continue

            if bracket_depth > 0:
                continue

            # Check if this token has any metadata possibilities
            has_metadata = bool(token.possibilities.keys() & cls.METADATA_LABELS)
            has_seq_only = (not has_metadata and
                            token.possibilities.keys() & cls.SEQUENCE_ONLY_LABELS == {Tag.SEQUENCE_NUMBER})

            # Delimiters — include in title if we're collecting
            if Tag.DELIMITER in token.possibilities and not has_metadata and not has_seq_only:
                if title_candidates and not found_metadata:
                    title_candidates.append(token)
                continue

            # Context delimiter (dash)
            if Tag.CONTEXT_DELIMITER in token.possibilities and not has_metadata and not has_seq_only:
                if title_candidates:
                    # Respect zone assignment: if this dash transitions to metadata zone, stop title
                    if token.zone == constant.ZONE_TRANSITION:
                        next_tok_zone = tokens.find_next(token)
                        while next_tok_zone and Tag.DELIMITER in next_tok_zone.possibilities:
                            next_tok_zone = tokens.find_next(next_tok_zone)
                        if next_tok_zone and next_tok_zone.zone == constant.ZONE_METADATA:
                            found_metadata = True
                            continue
                    next_tok = tokens.find_next(token)
                    # Look ahead: skip delimiters to find next meaningful token
                    while next_tok and Tag.DELIMITER in next_tok.possibilities:
                        next_tok = tokens.find_next(next_tok)
                    # Stop title if next token is a sequence prefix (like "episode", "ep")
                    if next_tok and Tag.SEQUENCE_PREFIX in next_tok.possibilities:
                        found_metadata = True
                        continue
                    if next_tok and Tag.SEQUENCE_NUMBER in next_tok.possibilities:
                        # But only stop if that next token has a prefix before it
                        has_prefix = False
                        prev = tokens.find_prev(next_tok)
                        while prev and Tag.DELIMITER in prev.possibilities:
                            prev = tokens.find_prev(prev)
                        if prev and (Tag.SEQUENCE_PREFIX in prev.possibilities or
                                     Tag.CONTEXT_DELIMITER in prev.possibilities):
                            has_prefix = True
                        if has_prefix:
                            found_metadata = True
                            continue
                    title_candidates.append(token)
                continue

            # Metadata token — title region is over
            if has_metadata:
                # Exception: single-char prefix after apostrophe is possessive, not metadata
                if (Tag.SEQUENCE_PREFIX in token.possibilities and len(token.content) == 1
                        and title_candidates and title_candidates[-1].content == constant.APOSTROPHE):
                    title_candidates.append(token)
                    continue
                # Exception: SEQUENCE_PREFIX after ordinal in title (e.g. "2nd season")
                # Only when followed by dash+number, not bare number
                if Tag.SEQUENCE_PREFIX in token.possibilities and title_candidates:
                    prev_meaningful = [t for t in title_candidates if Tag.DELIMITER not in t.possibilities]
                    if (prev_meaningful and cls._is_ordinal(prev_meaningful[-1].content, parser.config)
                            and cls._next_number_after_dash(token, tokens)):
                        title_candidates.append(token)
                        continue
                # Exception: TYPE or ambiguous labels in title flow without context delimiter
                # — no dash separating from previous title, preceded by plain text
                ambiguous_labels = token.possibilities.keys() & (cls.AMBIGUOUS_IN_TITLE | {Tag.TYPE})
                if (ambiguous_labels and title_candidates
                        and not cls._context_delim_before(token, tokens)
                        and cls._prev_is_unknown(token, tokens)):
                    title_candidates.append(token)
                    continue
                found_metadata = True
                if Tag.RELEASE_GROUP in token.possibilities:
                    found_metadata_type = Tag.RELEASE_GROUP
                elif Tag.LANGUAGE in token.possibilities or Tag.SUBS_TERM in token.possibilities:
                    found_metadata_type = Tag.LANGUAGE
                continue

            # Bare SEQUENCE_NUMBER: decide if it's title or episode
            if has_seq_only and (token.content.isdigit() or cls._is_ordinal(token.content, parser.config)):
                # Decimal continuation: if connected to previous title number via "."
                # (e.g., "1.0", "3.33"), always include in title
                if (title_candidates and len(title_candidates) >= 2
                        and Tag.DELIMITER in title_candidates[-1].possibilities
                        and title_candidates[-1].content == constant.DOT):
                    # Check if before the "." there was a SEQUENCE_NUMBER in title
                    prev_num = None
                    for tc in reversed(title_candidates[:-1]):
                        if Tag.DELIMITER in tc.possibilities:
                            continue
                        if Tag.SEQUENCE_NUMBER in tc.possibilities:
                            prev_num = tc
                        break
                    if prev_num is not None:
                        title_candidates.append(token)
                        continue
                # Ordinal followed by SEQUENCE_PREFIX = metadata (e.g. "2nd season 24")
                # unless next number is after a dash (e.g. "2nd season - 00")
                if cls._is_ordinal(token.content, parser.config):
                    next_meaningful = cls._next_meaningful_token(token, tokens)
                    if next_meaningful and Tag.SEQUENCE_PREFIX in next_meaningful.possibilities:
                        if not cls._next_number_after_dash(next_meaningful, tokens):
                            found_metadata = True
                            continue
                # If immediately preceded by TYPE keyword in title, this number is part of title
                # (e.g., "movie 2", "season 2") — but not "the tv 01"
                prev_type_in_title = False
                for t in reversed(title_candidates):
                    if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                        continue
                    if Tag.TYPE in t.possibilities:
                        prev_type_in_title = True
                    break
                if prev_type_in_title or cls._prev_is_title_number_continuation(title_candidates):
                    # Bare numbers after TYPE-in-title are title (e.g., "movie 9")
                    # Also numbers after connectors following title numbers (e.g., "movies 8 & 10")
                    # Zero-padded single digits are still episode (handled above)
                    is_zero_padded = (len(token.content) == 2
                                      and token.content[0] == '0'
                                      and token.content[1].isdigit())
                    if not is_zero_padded:
                        title_candidates.append(token)
                        continue
                # If previous title token is a short word glued directly to this number
                # (e.g., "R2", "S1", "ex01"), treat as compound title word
                if title_candidates:
                    prev_title = title_candidates[-1]
                    if (not prev_title.possibilities
                            and len(prev_title.content) <= 3
                            and prev_title.content.isalpha()
                            and prev_title.index + len(prev_title.content) == token.index):
                        title_candidates.append(token)
                        continue
                # Stop if preceded by structural prefix (like "ep", "episode", dash)
                # Glued dashes (no delimiter on either side) are not structural
                has_prefix = False
                for t in title_candidates[-3:]:
                    if not t:
                        continue
                    if Tag.SEQUENCE_PREFIX in t.possibilities:
                        has_prefix = True
                        break
                    if Tag.CONTEXT_DELIMITER in t.possibilities:
                        # Check if this dash is structural (has delimiter/space on at least one side)
                        t_end = t.index + len(t.content)
                        t_prev = None
                        t_next_tok = None
                        for tt in title_candidates:
                            if tt.index + len(tt.content) == t.index:
                                t_prev = tt
                            if tt.index == t_end:
                                t_next_tok = tt
                        is_structural = ((t_prev and Tag.DELIMITER in t_prev.possibilities) or
                                         (t_next_tok and Tag.DELIMITER in t_next_tok.possibilities))
                        if is_structural:
                            has_prefix = True
                            break
                if has_prefix:
                    found_metadata = True
                    continue
                # Look ahead: if non-metadata text follows, number is likely title
                # But zero-padded numbers (e.g. "03") are almost always episodes
                if not found_metadata and not token.content.startswith("0") and cls._has_text_after(token, tokens):
                    title_candidates.append(token)
                    continue
                # No text follows — but check if episode structure exists later
                # If so, this number is likely title (e.g. "fairy tail 2 - 52")
                if not found_metadata and cls._has_episode_after(token, tokens):
                    title_candidates.append(token)
                    continue
                # No text follows, no episode elsewhere — stop title
                # Exception: year-like numbers (4 digits, in year range) that are
                # glued to preceding text may be part of event names (e.g. "festa 2018")
                if not found_metadata:
                    if (len(token.content) == 4 and token.content.isdigit()
                            and 1900 <= int(token.content) <= 2099
                            and title_candidates
                            and not token.content.startswith("0")):
                        title_candidates.append(token)
                        continue
                    found_metadata = True
                    continue

            # Ambiguous SEQUENCE_PART (e.g. "d" in "3d"): include in title
            # if preceding token was included and text follows
            if (not found_metadata
                    and token.possibilities.keys() == {Tag.SEQUENCE_PART}
                    and title_candidates):
                title_candidates.append(token)
                continue

            # TYPE keyword (movie, special, gekijouban) in title zone:
            # include if followed eventually by unknown text, or if no structural
            # break (context delimiter) separates it from preceding title text
            if not found_metadata and Tag.TYPE in token.possibilities:
                # Inflected forms (OVAs, Movies, Specials) are title-leaning —
                # only metadata if bracket-isolated
                type_poss = token.possibilities[Tag.TYPE]
                if type_poss.element and type_poss.element.canonical and not token.bracket_group:
                    title_candidates.append(token)
                    continue
                # If TYPE is followed by a zero-padded number, it's metadata (e.g., "movie 02")
                # Bare numbers (9, 12) without context delimiter are title ("movie 9")
                next_meaningful = cls._next_meaningful_token(token, tokens)
                if next_meaningful and Tag.SEQUENCE_NUMBER in next_meaningful.possibilities:
                    is_zero_padded = (len(next_meaningful.content) == 2
                                      and next_meaningful.content[0] == '0'
                                      and next_meaningful.content[1].isdigit())
                    after_num = cls._next_meaningful_token(next_meaningful, tokens)
                    text_follows = after_num and not after_num.possibilities
                    has_article = title_candidates and cls._prev_is_article(title_candidates)
                    is_year = Tag.YEAR in next_meaningful.possibilities or Tag.SERIES_YEAR in next_meaningful.possibilities
                    if is_zero_padded and not text_follows and not has_article and not is_year:
                        found_metadata = True
                        continue
                if cls._has_unknown_text_eventually(token, tokens):
                    title_candidates.append(token)
                    continue
                # Include TYPE in title when no context delimiter separates it
                # from preceding plain text (e.g., "cells at work! special",
                # "aika zero ova - 01", "magical star kanon 100% OVA[DVD]")
                if (title_candidates
                        and not cls._context_delim_before(token, tokens)
                        and cls._prev_is_unknown(token, tokens)):
                    title_candidates.append(token)
                    continue
                # TYPE preceded by running title text and followed by bracket containing year:
                # e.g. "The Animated Movie (1994)" — "Movie" is part of the title
                if title_candidates and cls._prev_is_non_type_text(title_candidates):
                    next_m = cls._next_meaningful_token(token, tokens)
                    if next_m and Tag.BRACKET in next_m.possibilities:
                        # Check if the bracket group contains a year
                        if cls._bracket_contains_year(token_list, token_list.index(next_m)):
                            title_candidates.append(token)
                            continue
                # TYPE not followed by number, preceded by title text, followed by
                # context delimiter then non-numeric content → part of the title
                # (e.g., "school idol movie - pv" but NOT "ova - 01")
                if title_candidates and cls._context_delim_after(token, tokens):
                    # Check what follows the context delimiter
                    after_delim = cls._first_after_context_delim(token, tokens)
                    if after_delim and not (Tag.SEQUENCE_NUMBER in after_delim.possibilities):
                        title_candidates.append(token)
                        continue
                # TYPE without text after = metadata boundary
                found_metadata = True
                continue

            if found_metadata:
                # If no title collected yet and we see unknown text after release group,
                # restart title search (e.g., ]akihitosubs] elfen lied...)
                if (not title_candidates and not token.possibilities
                        and found_metadata_type in (Tag.RELEASE_GROUP, Tag.LANGUAGE)):
                    found_metadata = False
                    found_metadata_type = None
                    # fall through to unknown token handling below
                else:
                    continue

            # CONTEXT_DEPENDENT (e.g., "&") — include in title when between title tokens
            if (Tag.CONTEXT_DEPENDENT in token.possibilities and title_candidates
                    and not found_metadata):
                title_candidates.append(token)
                continue

            # Empty possibilities = UNKNOWN token
            if not token.possibilities:
                if token is extension_token:
                    continue
                title_candidates.append(token)

        # Trim trailing/leading delimiters
        while title_candidates and Tag.DELIMITER in title_candidates[-1].possibilities:
            title_candidates.pop()
        while title_candidates and Tag.DELIMITER in title_candidates[0].possibilities:
            title_candidates.pop(0)
        while title_candidates and Tag.CONTEXT_DELIMITER in title_candidates[-1].possibilities:
            title_candidates.pop()
        while title_candidates and Tag.CONTEXT_DELIMITER in title_candidates[0].possibilities:
            title_candidates.pop(0)

        # Apply TITLE possibility
        for token in title_candidates:
            if not token.possibilities:
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.0)
            elif Tag.BRACKET in token.possibilities:
                # Bracket included in title (e.g., "[not]", "(not)")
                token.add_possibility(Tag.SERIES_TITLE, base_score=0.5)
            elif Tag.RELEASE_GROUP in token.possibilities and not (token.possibilities.keys() & cls.METADATA_LABELS - {Tag.RELEASE_GROUP}):
                # Release group candidate inside bracket that's part of title
                # But if release_group_rule already gave it a high score, don't override
                rg_score = token.possibilities[Tag.RELEASE_GROUP].score
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.0 if rg_score >= 1.5 else 1.5)
            elif Tag.DELIMITER in token.possibilities or Tag.CONTEXT_DELIMITER in token.possibilities:
                token.add_possibility(Tag.SERIES_TITLE, base_score=0.5)
            elif token.possibilities.keys() & cls.SEQUENCE_ONLY_LABELS:
                # Bare number included in title — add TITLE as competing possibility
                # Higher score (1.5) because heuristic determined it's likely title
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.5)
            elif token.possibilities.keys() == {Tag.SEQUENCE_PART}:
                # Ambiguous part suffix included in title (e.g. "d" in "3d")
                token.add_possibility(Tag.SERIES_TITLE, base_score=2.0)
            elif Tag.TYPE in token.possibilities:
                # TYPE keyword included in title (e.g. "gekijouban", "movie" as part of title)
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.5)
            elif Tag.SEQUENCE_PREFIX in token.possibilities:
                # Possessive 's or other prefix included in title context
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.5)
            elif token.possibilities.keys() & cls.AMBIGUOUS_IN_TITLE:
                # Ambiguous keyword included in title flow (e.g. "ita" in "bokura ga ita")
                # Use moderate score — regex-confirmed keywords (1.5) should override
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.0)
            elif Tag.CONTEXT_DEPENDENT in token.possibilities:
                # Context-dependent tokens like "&" included in title
                token.add_possibility(Tag.SERIES_TITLE, base_score=1.5)

        # If no title found by first pass, check for bracket-enclosed title
        if not title_candidates:
            cls._detect_bracket_title(tokens)

        # Second pass: detect episode titles (UNKNOWN tokens after last SEQUENCE_NUMBER, outside brackets)
        cls._detect_episode_title(tokens, extension_token)

        # Third pass: detect episode title in brackets immediately after episode number
        cls._detect_bracket_episode_title(tokens)

    @staticmethod
    def _get_title_bracket_content(token_list, open_idx, metadata_labels):
        """Check if bracket content should be included in title.

        Returns (list of tokens, close_idx) if the bracket content has no metadata
        and text follows, or (None, -1) if it should not be included.
        """
        open_tok = token_list[open_idx]
        inside = []
        close_idx = None
        expected_close = constant.BRACKET_PAIRS.get(open_tok.content)
        for j in range(open_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.BRACKET in t.possibilities and t.content == expected_close:
                close_idx = j
                break
            inside.append(t)
        if close_idx is None or not inside:
            return None, -1
        # Check if any inside token has metadata possibilities
        # Check if bracket contains metadata (→ not title content).
        # RELEASE_GROUP alone is not considered metadata — it could be a title word.
        # If the bracket has a mix of unknown and low-confidence metadata tokens,
        # it's likely title content (e.g., "the final season" where "season" is a keyword).
        meaningful = [t for t in inside
                      if Tag.DELIMITER not in t.possibilities
                      and Tag.CONTEXT_DELIMITER not in t.possibilities]
        metadata_count = 0
        for t in meaningful:
            non_rg_metadata = t.possibilities.keys() & metadata_labels - {Tag.RELEASE_GROUP}
            if non_rg_metadata:
                metadata_count += 1
            rg_poss = t.possibilities.get(Tag.RELEASE_GROUP)
            if rg_poss and rg_poss.score >= 1.5:
                return None, -1
        # Reject if all meaningful tokens are metadata (e.g., "(TV)", "(2008)", "(DVD)")
        if meaningful and metadata_count == len(meaningful):
            return None, -1
        # Check if this bracket belongs in the title:
        # (a) title text follows, (b) bracket is glued to preceding title,
        # or (c) context delimiter follows (indicating episode/metadata after title)
        has_text_after = False
        has_context_delim_after = False
        for j in range(close_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.DELIMITER in t.possibilities and Tag.CONTEXT_DELIMITER not in t.possibilities:
                continue
            if Tag.CONTEXT_DELIMITER in t.possibilities:
                has_context_delim_after = True
                break
            if Tag.BRACKET in t.possibilities:
                break
            if not t.possibilities:
                has_text_after = True
            break
        # Check if bracket is glued (no delimiter between last title token and open bracket)
        is_glued = (open_idx > 0 and
                    Tag.DELIMITER not in token_list[open_idx - 1].possibilities and
                    Tag.BRACKET not in token_list[open_idx - 1].possibilities)
        if not has_text_after and not is_glued and not has_context_delim_after:
            return None, -1
        result = [open_tok] + inside + [token_list[close_idx]]
        return result, close_idx

    @classmethod
    def _prev_is_title_number_continuation(cls, title_candidates):
        """Check if title candidates end with a connector after a number (e.g., '8 &').

        This detects the pattern TYPE + number + connector, where the next number
        should also be part of the title (e.g., 'movies 8 & 10').
        """
        # Walk back: expect connector, then digit
        state = 'expect_connector'
        for t in reversed(title_candidates):
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                continue
            if state == 'expect_connector' and Tag.CONTEXT_DEPENDENT in t.possibilities:
                state = 'expect_digit'
                continue
            if state == 'expect_digit' and t.content.isdigit():
                return True
            return False
        return False

    @classmethod
    def _prev_is_article(cls, title_candidates):
        """Check if the last non-delimiter title candidate is a short lowercase function word.

        Articles and prepositions in titles are typically lowercase and short
        (e.g., "the", "no", "of"). When such a word directly precedes a TYPE
        keyword, the TYPE is likely part of the title (e.g., "the movie").
        Uppercase words like "Z" or content words like "work" don't qualify.
        """
        for t in reversed(title_candidates):
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                continue
            return (not t.possibilities
                    and t.content.islower()
                    and 2 <= len(t.content) <= 3)
        return False

    @classmethod
    def _has_text_after(cls, token, tokens):
        """Check if non-metadata UNKNOWN text follows this token before next structural break."""
        next_tok = tokens.find_next(token)
        # Skip delimiters, ambiguous sequence parts, and decimal-connected numbers
        while next_tok and (Tag.DELIMITER in next_tok.possibilities
                            or next_tok.possibilities.keys() == {Tag.SEQUENCE_PART}):
            next_tok = tokens.find_next(next_tok)
        # Skip decimal-connected SEQUENCE_NUMBER (e.g., "3" "." "33" → look past "33")
        if (next_tok and next_tok.possibilities.keys() & cls.SEQUENCE_ONLY_LABELS
                and next_tok.content.isdigit()):
            prev = tokens.find_prev(next_tok)
            if prev and Tag.DELIMITER in prev.possibilities and prev.content == constant.DOT:
                # This number is connected via "." to the previous — treat as decimal, skip
                next_tok = tokens.find_next(next_tok)
                while next_tok and (Tag.DELIMITER in next_tok.possibilities
                                    or next_tok.possibilities.keys() == {Tag.SEQUENCE_PART}):
                    next_tok = tokens.find_next(next_tok)
        if not next_tok:
            return False
        # Unknown token, TYPE-only, or TITLE = text continues
        if not next_tok.possibilities or next_tok.possibilities.keys() == {Tag.TYPE}:
            return True
        if Tag.TITLE in next_tok.possibilities:
            return True
        # Context delimiter (dash) — check what follows
        if Tag.CONTEXT_DELIMITER in next_tok.possibilities:
            # Look past the dash for either episode structure or plain text
            # Only include as title if the number doesn't look like an episode
            # (no leading zero) and text follows the dash
            if not token.content.startswith("0"):
                past_dash = tokens.find_next(next_tok)
                while past_dash and Tag.DELIMITER in past_dash.possibilities:
                    past_dash = tokens.find_next(past_dash)
                if past_dash and not past_dash.possibilities:
                    return True  # Plain unknown text after dash
            return cls._has_episode_after(next_tok, tokens)
        # Bracket — look past it for episode evidence
        if Tag.BRACKET in next_tok.possibilities:
            return cls._has_episode_after(next_tok, tokens)
        # Sequence prefix after this number means episode is elsewhere
        if Tag.SEQUENCE_PREFIX in next_tok.possibilities:
            return True
        # Other metadata = structural break
        if next_tok.possibilities.keys() & cls.METADATA_LABELS:
            return False
        if next_tok.possibilities.keys() & cls.SEQUENCE_ONLY_LABELS:
            return False
        return False

    @classmethod
    def _has_episode_after(cls, start_tok, tokens):
        """Check if there's episode structure (prefix+number or dash+number) after this point."""
        tok = start_tok
        in_bracket = False
        after_dash = Tag.CONTEXT_DELIMITER in start_tok.possibilities
        while tok:
            tok = tokens.find_next(tok)
            if not tok:
                return False
            if Tag.BRACKET in tok.possibilities:
                if tok.content in constant.OPEN_BRACKETS:
                    in_bracket = True
                elif tok.content in constant.CLOSE_BRACKETS:
                    in_bracket = False
                continue
            if in_bracket:
                continue
            if Tag.DELIMITER in tok.possibilities:
                continue
            # Found a sequence prefix outside brackets — episode exists later
            if Tag.SEQUENCE_PREFIX in tok.possibilities:
                return True
            # Found a context delimiter — mark it, look for number after
            if Tag.CONTEXT_DELIMITER in tok.possibilities:
                after_dash = True
                continue
            # Number after a dash = episode evidence (but not release version like "v2")
            if after_dash and Tag.SEQUENCE_NUMBER in tok.possibilities:
                if Tag.RELEASE_VERSION not in tok.possibilities:
                    return True
            after_dash = False
        return False

    @classmethod
    def _detect_episode_title(cls, tokens, extension_token):
        """Tag UNKNOWN tokens after the last SEQUENCE_NUMBER as episode title."""
        token_list = tokens.tokens
        last_seq_idx = -1
        in_bracket = False
        for i, token in enumerate(token_list):
            if Tag.BRACKET in token.possibilities:
                if token.content in constant.OPEN_BRACKETS:
                    in_bracket = True
                elif token.content in constant.CLOSE_BRACKETS:
                    in_bracket = False
                continue
            if in_bracket:
                continue
            if Tag.SEQUENCE_NUMBER in token.possibilities:
                last_seq_idx = i
        anchor_idx = last_seq_idx
        stop_before_idx = -1  # if backed up, don't include the original last seq token
        anchor_backed_up = False

        # If the last SEQUENCE_NUMBER is embedded in text (UNKNOWN on both sides),
        # step back to the previous SEQUENCE_NUMBER as anchor
        if anchor_idx >= 0:
            anchor_tok = token_list[anchor_idx]
            has_unknown_before = False
            has_unknown_after = False
            for j in range(anchor_idx - 1, -1, -1):
                t = token_list[j]
                if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                    continue
                if not t.possibilities or Tag.TITLE in t.possibilities:
                    has_unknown_before = True
                break
            for j in range(anchor_idx + 1, len(token_list)):
                t = token_list[j]
                if Tag.DELIMITER in t.possibilities:
                    continue
                if Tag.BRACKET in t.possibilities:
                    break
                if not t.possibilities:
                    has_unknown_after = True
                break
            if has_unknown_before:
                # Find previous SEQUENCE_NUMBER outside brackets
                prev_seq_idx = -1
                in_bracket2 = False
                for j in range(anchor_idx - 1, -1, -1):
                    t = token_list[j]
                    if Tag.BRACKET in t.possibilities:
                        if t.content in constant.CLOSE_BRACKETS:
                            in_bracket2 = True
                        elif t.content in constant.OPEN_BRACKETS:
                            in_bracket2 = False
                        continue
                    if in_bracket2:
                        continue
                    if Tag.SEQUENCE_NUMBER in t.possibilities:
                        prev_seq_idx = j
                        break
                if prev_seq_idx >= 0:
                    anchor_backed_up = True
                    if not has_unknown_after:
                        # Stop before the last seq number if preceded by a structural
                        # context delimiter (dash with spaces around it)
                        has_context_delim_before = False
                        for j in range(anchor_idx - 1, -1, -1):
                            t = token_list[j]
                            if Tag.DELIMITER in t.possibilities and Tag.CONTEXT_DELIMITER not in t.possibilities:
                                continue
                            if Tag.CONTEXT_DELIMITER in t.possibilities:
                                has_context_delim_before = True
                            break
                        if has_context_delim_before:
                            stop_before_idx = anchor_idx
                    anchor_idx = prev_seq_idx

        if anchor_idx < 0:
            return

        # Collect UNKNOWN tokens after anchor sequence number, outside brackets
        ep_title_candidates = []
        in_bracket = False
        for i in range(anchor_idx + 1, len(token_list)):
            token = token_list[i]
            if Tag.BRACKET in token.possibilities:
                if token.content in constant.OPEN_BRACKETS:
                    in_bracket = True
                elif token.content in constant.CLOSE_BRACKETS:
                    in_bracket = False
                continue
            if in_bracket:
                continue
            if token is extension_token:
                continue

            has_seq = Tag.SEQUENCE_NUMBER in token.possibilities
            has_metadata = bool(token.possibilities.keys() & (cls.METADATA_LABELS - {Tag.FILE_INDEX}))
            # SEQUENCE_NUMBER inside episode title: check before metadata break
            if has_seq and not has_metadata:
                # Stop before the original last seq number when anchor was backed up
                if stop_before_idx >= 0 and i >= stop_before_idx:
                    break
                if ep_title_candidates:
                    if cls._has_unknown_text_after_in_eptitle(token, token_list, i, extension_token):
                        ep_title_candidates.append(token)
                        continue
                    # Number at the end of episode title (only brackets/delimiters follow)
                    if cls._only_brackets_after(token_list, i, extension_token):
                        ep_title_candidates.append(token)
                        continue
                break
            if has_metadata:
                # Content keywords (opening, ending, part) can be part of episode title
                if ep_title_candidates and cls._is_content_keyword(token):
                    ep_title_candidates.append(token)
                    continue
                # Possessive 's: single "s" right after apostrophe is not a real prefix
                if (Tag.SEQUENCE_PREFIX in token.possibilities
                        and len(token.content) == 1
                        and ep_title_candidates
                        and ep_title_candidates[-1].content == constant.APOSTROPHE):
                    ep_title_candidates.append(token)
                    continue
                break  # hit metadata, stop

            if (not token.possibilities or token.possibilities.keys() == {Tag.CONTEXT_DEPENDENT}
                    or (token.possibilities.keys() == {Tag.TITLE})):
                ep_title_candidates.append(token)
            elif token.possibilities.keys() <= {Tag.FILE_INDEX} and ep_title_candidates:
                # Small number (FILE_INDEX) after text — include in episode title (e.g. "part 1")
                ep_title_candidates.append(token)
            elif Tag.DELIMITER in token.possibilities or Tag.CONTEXT_DELIMITER in token.possibilities:
                if ep_title_candidates:
                    ep_title_candidates.append(token)
                elif not token.possibilities.keys() - {Tag.DELIMITER, Tag.CONTEXT_DELIMITER}:
                    # Plain delimiter before any ep title tokens — skip but don't break
                    continue
            elif Tag.TYPE in token.possibilities:
                # TYPE in episode title zone: treat as title text (e.g., "special day")
                ep_title_candidates.append(token)
            elif ep_title_candidates and cls._is_content_keyword(token):
                # Content keywords (e.g. "opening", "part") can be part of episode title
                ep_title_candidates.append(token)
            elif not ep_title_candidates and cls._is_content_keyword(token):
                # Content keywords before any text — skip, might start ep title after
                continue

        # Trim trailing/leading delimiters
        while ep_title_candidates and (Tag.DELIMITER in ep_title_candidates[-1].possibilities or Tag.CONTEXT_DELIMITER in ep_title_candidates[-1].possibilities):
            ep_title_candidates.pop()
        while ep_title_candidates and (Tag.DELIMITER in ep_title_candidates[0].possibilities or Tag.CONTEXT_DELIMITER in ep_title_candidates[0].possibilities):
            ep_title_candidates.pop(0)

        if not ep_title_candidates:
            return

        # Don't tag as episode title if already tagged as series title
        # (unless anchor was backed up, meaning these are between season and episode)
        if not anchor_backed_up:
            for token in ep_title_candidates:
                if Tag.TITLE in token.possibilities:
                    return

        for ti, token in enumerate(ep_title_candidates):
            if (not token.possibilities or token.possibilities.keys() == {Tag.CONTEXT_DEPENDENT}
                    or token.possibilities.keys() == {Tag.TITLE}):
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=1.0)
            elif Tag.SEQUENCE_NUMBER in token.possibilities:
                # Number embedded in episode title (e.g., "data_01_login")
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=1.5)
            elif Tag.DELIMITER in token.possibilities or Tag.CONTEXT_DELIMITER in token.possibilities:
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=0.5)
            elif cls._is_content_keyword(token):
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=2.0)
            elif (Tag.SEQUENCE_PREFIX in token.possibilities and len(token.content) == 1
                  and ti > 0 and ep_title_candidates[ti - 1].content == constant.APOSTROPHE):
                # Possessive 's — include in episode title
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=2.0)
            elif token.possibilities.keys() <= {Tag.FILE_INDEX}:
                # Small number included in episode title (e.g. "part 1")
                token.add_possibility(Tag.SEQUENCE_TITLE, base_score=1.5)

    @classmethod
    def _only_brackets_after(cls, token_list, current_idx, extension_token):
        """Check if only brackets, delimiters, and extension follow this token."""
        for j in range(current_idx + 1, len(token_list)):
            t = token_list[j]
            if t is extension_token:
                continue
            if Tag.DELIMITER in t.possibilities:
                continue
            if Tag.BRACKET in t.possibilities:
                return True
            return False  # something else follows
        return True  # end of tokens

    @classmethod
    def _has_unknown_text_after_in_eptitle(cls, token, token_list, current_idx, extension_token):
        """Check if unknown text follows this SEQUENCE_NUMBER in the episode title context."""
        for j in range(current_idx + 1, len(token_list)):
            t = token_list[j]
            if t is extension_token:
                continue
            if Tag.BRACKET in t.possibilities:
                return False
            if Tag.DELIMITER in t.possibilities:
                continue
            if not t.possibilities:
                return True  # Unknown text follows
            return False
        return False

    @classmethod
    def _has_unknown_text_eventually(cls, token, tokens):
        """Check if unknown text follows, looking past numbers, delimiters, and context delimiters."""
        next_tok = tokens.find_next(token)
        while next_tok and (Tag.DELIMITER in next_tok.possibilities
                            or Tag.CONTEXT_DELIMITER in next_tok.possibilities
                            or Tag.SEQUENCE_NUMBER in next_tok.possibilities):
            next_tok = tokens.find_next(next_tok)
        if not next_tok:
            return False
        if Tag.BRACKET in next_tok.possibilities:
            return False
        return not next_tok.possibilities

    @classmethod
    def _has_unknown_text_after(cls, token, tokens):
        """Check if truly unknown (no possibilities) text follows this token."""
        next_tok = tokens.find_next(token)
        while next_tok and (Tag.DELIMITER in next_tok.possibilities
                            or Tag.CONTEXT_DELIMITER in next_tok.possibilities):
            next_tok = tokens.find_next(next_tok)
        if not next_tok:
            return False
        return not next_tok.possibilities

    @classmethod
    def _next_meaningful_token(cls, token, tokens):
        """Find next non-delimiter token."""
        tok = tokens.find_next(token)
        while tok and Tag.DELIMITER in tok.possibilities:
            tok = tokens.find_next(tok)
        return tok

    @classmethod
    def _next_number_after_dash(cls, token, tokens):
        """Check if the next SEQUENCE_NUMBER is preceded by a context delimiter (dash)."""
        tok = tokens.find_next(token)
        while tok and Tag.DELIMITER in tok.possibilities:
            tok = tokens.find_next(tok)
        if not tok:
            return False
        # If next meaningful token is a context delimiter, the number follows after
        if Tag.CONTEXT_DELIMITER in tok.possibilities:
            return True
        # If next meaningful token is a bare number (no dash), return False
        return False

    @staticmethod
    def _is_ordinal(content: str, config=None) -> bool:
        """Check if token is an ordinal number like '1st', '2nd', '3rd', '4th'."""
        if config and config.ordinal_suffixes:
            lower = content.lower()
            for suffix in config.ordinal_suffixes:
                if lower.endswith(suffix) and lower[:-len(suffix)].isdigit():
                    return True
            return False
        from aniparse.rule.possibilities.number_rule import get_number_from_ordinal
        from aniparse.config import ParserConfig
        return bool(get_number_from_ordinal(content, ParserConfig()))

    @staticmethod
    def _bracket_contains_year(token_list, open_idx):
        """Check if a bracket group starting at open_idx contains a YEAR token."""
        for j in range(open_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.BRACKET in t.possibilities and t.content in constant.CLOSE_BRACKETS:
                break
            if Tag.YEAR in t.possibilities or Tag.SERIES_YEAR in t.possibilities:
                return True
        return False

    @classmethod
    def _prev_is_non_type_text(cls, title_candidates):
        """Check if the last non-delimiter title candidate is plain text (not TYPE or article)."""
        for t in reversed(title_candidates):
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                continue
            # Must be plain unknown text (no TYPE possibility) and not a function word
            if not t.possibilities and t.content.islower() and 2 <= len(t.content) <= 3:
                return False
            return not t.possibilities or (Tag.TYPE not in t.possibilities)
        return False

    @classmethod
    def _prev_is_unknown(cls, token, tokens):
        """Check if the previous non-delimiter token has no possibilities (plain text)."""
        prev = tokens.find_prev(token)
        while prev and Tag.DELIMITER in prev.possibilities:
            prev = tokens.find_prev(prev)
        if not prev:
            return False
        return not prev.possibilities

    @classmethod
    @classmethod
    def _followed_by_structural_break(cls, token, tokens):
        """Check if a context delimiter, bracket, or end-of-tokens follows this token."""
        nxt = tokens.find_next(token)
        while nxt and Tag.DELIMITER in nxt.possibilities:
            nxt = tokens.find_next(nxt)
        if not nxt:
            return False  # end of tokens — no structural break
        return (Tag.CONTEXT_DELIMITER in nxt.possibilities
                or Tag.BRACKET in nxt.possibilities)

    @classmethod
    def _context_delim_before(cls, token, tokens):
        """Check if a context delimiter exists between this token and its previous non-delimiter neighbor."""
        prev = tokens.find_prev(token)
        while prev and Tag.DELIMITER in prev.possibilities:
            prev = tokens.find_prev(prev)
        if prev and Tag.CONTEXT_DELIMITER in prev.possibilities:
            return True
        return False

    @staticmethod
    def _is_content_keyword(token):
        """Check if a token is a content keyword (CONTENT_TYPE, CONTENT_IDENTIFIER, or SEQUENCE_PREFIX with content descriptor)."""
        if Tag.CONTENT_TYPE in token.possibilities or Tag.CONTENT_IDENTIFIER in token.possibilities:
            return True
        poss = token.possibilities.get(Tag.SEQUENCE_PREFIX)
        if poss and poss.descriptor in (Tag.CONTENT_TYPE, Tag.CONTENT_IDENTIFIER):
            return True
        return False

    @classmethod
    def _number_immediately_after(cls, token, tokens):
        """Check if the next non-delimiter token is a SEQUENCE_NUMBER."""
        nxt = tokens.find_next(token)
        while nxt and Tag.DELIMITER in nxt.possibilities and Tag.SEQUENCE_NUMBER not in nxt.possibilities:
            nxt = tokens.find_next(nxt)
        if nxt and Tag.SEQUENCE_NUMBER in nxt.possibilities:
            return True
        return False

    @classmethod
    def _context_delim_after(cls, token, tokens):
        """Check if a context delimiter exists after this token (skipping plain delimiters)."""
        nxt = tokens.find_next(token)
        while nxt and Tag.DELIMITER in nxt.possibilities and Tag.CONTEXT_DELIMITER not in nxt.possibilities:
            nxt = tokens.find_next(nxt)
        if nxt and Tag.CONTEXT_DELIMITER in nxt.possibilities:
            return True
        return False

    @classmethod
    def _first_after_context_delim(cls, token, tokens):
        """Find the first meaningful token after the next context delimiter."""
        nxt = tokens.find_next(token)
        found_delim = False
        while nxt:
            if Tag.CONTEXT_DELIMITER in nxt.possibilities:
                found_delim = True
            elif Tag.DELIMITER in nxt.possibilities:
                pass
            elif found_delim:
                return nxt
            else:
                break
            nxt = tokens.find_next(nxt)
        return None

    @staticmethod
    def _has_unknown_after_bracket(token_list, open_idx):
        """Check if unknown text follows after the bracket group starting at open_idx."""
        open_tok = token_list[open_idx]
        expected_close = constant.BRACKET_PAIRS.get(open_tok.content)
        close_idx = None
        for j in range(open_idx + 1, len(token_list)):
            if Tag.BRACKET in token_list[j].possibilities and token_list[j].content == expected_close:
                close_idx = j
                break
        if close_idx is None:
            return False
        for j in range(close_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.DELIMITER in t.possibilities:
                continue
            return not t.possibilities  # True if unknown text, False otherwise
        return False

    @staticmethod
    def _bracket_has_release_group(token_list, open_idx):
        """Check if bracket content is a release group (has RELEASE_GROUP possibility)."""
        open_tok = token_list[open_idx]
        expected_close = constant.BRACKET_PAIRS.get(open_tok.content)
        for j in range(open_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.BRACKET in t.possibilities and t.content == expected_close:
                break
            if Tag.RELEASE_GROUP in t.possibilities:
                return True
        return False

    @staticmethod
    def _find_extension_token(tokens):
        """Find the file extension token — last UNKNOWN after last dot."""
        all_tokens = tokens.tokens
        if len(all_tokens) < 3:
            return None
        last = all_tokens[-1]
        second_last = all_tokens[-2]
        if (not last.possibilities
                and Tag.DELIMITER in second_last.possibilities
                and second_last.content == constant.DOT):
            return last
        return None

    @classmethod
    def _detect_bracket_title(cls, tokens):
        """Detect title inside a bracket group when no outside-bracket title was found.

        Pattern: [release_group][long title text] ep02 [metadata]
        A bracket group with many unknown words before episode markers is a title.
        """
        token_list = tokens.tokens

        # Find bracket groups
        bracket_groups = []
        i = 0
        while i < len(token_list):
            t = token_list[i]
            if Tag.BRACKET in t.possibilities and t.content in constant.OPEN_BRACKETS:
                inside = []
                close_idx = None
                expected_close = constant.BRACKET_PAIRS.get(t.content)
                for j in range(i + 1, len(token_list)):
                    tj = token_list[j]
                    if Tag.BRACKET in tj.possibilities and tj.content == expected_close:
                        close_idx = j
                        break
                    inside.append(tj)
                if close_idx is not None:
                    bracket_groups.append((i, inside, close_idx))
                    i = close_idx + 1
                    continue
            i += 1

        if len(bracket_groups) < 2:
            return

        # Look for a bracket group that:
        # (a) contains mostly unknown text (>4 non-delimiter words)
        # (b) is followed by episode markers or end of filename
        for bg_idx, (open_idx, inside, close_idx) in enumerate(bracket_groups):
            if bg_idx == 0:
                continue  # skip first (likely release_group)

            word_tokens = [t for t in inside
                           if Tag.DELIMITER not in t.possibilities
                           and Tag.CONTEXT_DELIMITER not in t.possibilities]
            if len(word_tokens) < 4:
                continue

            # Check: mostly unknown tokens (no strong metadata)
            unknown_count = 0
            metadata_count = 0
            for t in word_tokens:
                if not t.possibilities or Tag.RELEASE_GROUP in t.possibilities:
                    unknown_count += 1
                elif t.possibilities.keys() & (cls.METADATA_LABELS | {Tag.SEQUENCE_NUMBER}):
                    metadata_count += 1
                else:
                    unknown_count += 1

            if unknown_count < 4 or metadata_count > unknown_count:
                continue

            # Check what follows: episode markers, bracket metadata, or end
            has_episode_after = False
            has_metadata_bracket_after = False
            for j in range(close_idx + 1, len(token_list)):
                t = token_list[j]
                if Tag.DELIMITER in t.possibilities:
                    continue
                if Tag.SEQUENCE_PREFIX in t.possibilities:
                    has_episode_after = True
                if Tag.SEQUENCE_NUMBER in t.possibilities:
                    has_episode_after = True
                if Tag.BRACKET in t.possibilities and t.content in constant.OPEN_BRACKETS:
                    has_metadata_bracket_after = True
                break

            # Allow bracket title when episodes follow, or when only metadata brackets follow
            # (e.g., [group][title][480p][v0])
            if not has_episode_after and not has_metadata_bracket_after:
                continue

            # Tag inside tokens as title — use high scores to override false metadata
            for t in inside:
                if not t.possibilities:
                    t.add_possibility(Tag.SERIES_TITLE, base_score=2.0)
                elif Tag.BRACKET in t.possibilities:
                    t.add_possibility(Tag.SERIES_TITLE, base_score=0.5)
                elif Tag.DELIMITER in t.possibilities and (not t.content.strip() or t.content == constant.UNDERSCORE):
                    t.add_possibility(Tag.SERIES_TITLE, base_score=0.5)
                else:
                    # Override any metadata (audio_term, sequence_number, release_group, etc.)
                    t.add_possibility(Tag.SERIES_TITLE, base_score=2.0)
            # Also tag the bracket tokens themselves for compose to handle
            token_list[open_idx].add_possibility(Tag.SERIES_TITLE, base_score=0.5)
            token_list[close_idx].add_possibility(Tag.SERIES_TITLE, base_score=0.5)
            return  # only one bracket title

    @classmethod
    def _detect_bracket_episode_title(cls, tokens):
        """Detect episode title inside brackets immediately after episode number.

        Pattern: ... 13v0 (uncensored director's cut) [metadata] ...
        If a bracket group right after the last episode contains mostly unknown tokens,
        tag them as episode title.
        """
        token_list = tokens.tokens
        # Find last SEQUENCE_NUMBER outside brackets
        last_seq_idx = -1
        in_bracket = False
        for i, token in enumerate(token_list):
            if Tag.BRACKET in token.possibilities:
                if token.content in constant.OPEN_BRACKETS:
                    in_bracket = True
                elif token.content in constant.CLOSE_BRACKETS:
                    in_bracket = False
                continue
            if in_bracket:
                continue
            if Tag.SEQUENCE_NUMBER in token.possibilities:
                last_seq_idx = i

        if last_seq_idx < 0:
            return

        # Already has episode title from _detect_episode_title? Skip.
        for token in token_list[last_seq_idx + 1:]:
            if Tag.TITLE in token.possibilities:
                poss = token.possibilities.get(Tag.TITLE)
                if poss and poss.descriptor == Tag.SEQUENCE_TITLE:
                    return

        # Find first bracket group after last episode (skip delimiters, release_version)
        open_idx = None
        for i in range(last_seq_idx + 1, len(token_list)):
            t = token_list[i]
            if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                continue
            if Tag.RELEASE_VERSION in t.possibilities:
                continue
            if Tag.BRACKET in t.possibilities and t.content in constant.OPEN_BRACKETS:
                open_idx = i
                break
            break  # non-bracket, non-delimiter found → no bracket ep title

        if open_idx is None:
            return

        # Collect tokens inside this bracket
        inside = []
        close_idx = None
        expected_close = constant.BRACKET_PAIRS.get(token_list[open_idx].content)
        for j in range(open_idx + 1, len(token_list)):
            t = token_list[j]
            if Tag.BRACKET in t.possibilities and t.content == expected_close:
                close_idx = j
                break
            inside.append(t)

        if not inside or close_idx is None:
            return

        # Only parenthesized brackets, not square/curly (those are metadata/release_group)
        if token_list[open_idx].content not in constant.OPEN_PARENS:
            return

        # Check: all non-delimiter tokens must be unknown or RELEASE_INFORMATION
        # (no video_term, audio_term, source, resolution, sequence_number, etc.)
        _hard_metadata = {Tag.VIDEO_TERM, Tag.AUDIO_TERM, Tag.SOURCE, Tag.VIDEO_RESOLUTION,
                          Tag.FILE_CHECKSUM, Tag.SEQUENCE_NUMBER, Tag.SEQUENCE_PREFIX,
                          Tag.LANGUAGE, Tag.SUBS_TERM}
        unknown_count = 0
        for ti, t in enumerate(inside):
            if Tag.DELIMITER in t.possibilities:
                continue
            # Possessive 's after apostrophe is not real metadata
            is_possessive_s = (Tag.SEQUENCE_PREFIX in t.possibilities
                               and len(t.content) == 1 and ti > 0
                               and inside[ti - 1].content == constant.APOSTROPHE)
            if not is_possessive_s and t.possibilities.keys() & _hard_metadata:
                return  # has real metadata → not an episode title
            unknown_count += 1

        if unknown_count == 0:
            return

        # Skip if all inside tokens already have RELEASE_GROUP possibility
        # (the bracket is likely a release group, not episode title)
        all_rg = all(
            Tag.RELEASE_GROUP in t.possibilities or Tag.DELIMITER in t.possibilities
            for t in inside
        )
        if all_rg:
            return

        # Require at least one RELEASE_INFORMATION token to distinguish from release groups
        # (episode titles in brackets usually have words like "uncensored", "uncut", etc.)
        has_release_info = any(Tag.RELEASE_INFORMATION in t.possibilities for t in inside)
        if not has_release_info:
            return

        # Tag all inside tokens as episode title
        for ti, t in enumerate(inside):
            if not t.possibilities:
                t.add_possibility(Tag.SEQUENCE_TITLE, base_score=1.0)
            elif Tag.RELEASE_INFORMATION in t.possibilities:
                t.add_possibility(Tag.SEQUENCE_TITLE, base_score=2.0)
            elif Tag.DELIMITER in t.possibilities:
                t.add_possibility(Tag.SEQUENCE_TITLE, base_score=0.5)
            elif (Tag.SEQUENCE_PREFIX in t.possibilities and len(t.content) == 1
                  and ti > 0 and inside[ti - 1].content == constant.APOSTROPHE):
                # Possessive 's — include in episode title
                t.add_possibility(Tag.SEQUENCE_TITLE, base_score=2.0)
