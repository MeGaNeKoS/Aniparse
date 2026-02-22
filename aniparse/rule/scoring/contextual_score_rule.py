"""Score adjustments based on token rhythm and surrounding context.

Key principle: context delimiters (dashes) are the strongest structural signal.
A keyword token flowing in title-zone text without structural separation is
likely part of the title, not metadata.
"""
from aniparse.core.constant import ZONE_TITLE, ZONE_METADATA
from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token import Token, Tokens
from aniparse.core.token_tags import Tag

# Labels that can be false positives in title context
AMBIGUOUS_IN_TITLE = {
    Tag.LANGUAGE, Tag.SUBS_TERM, Tag.RELEASE_INFORMATION,
    Tag.EXTRA_INFO,
}


class ContextualScoreRule(ScoreRule):
    """Penalize ambiguous metadata labels when token is in title flow.

    A token is in "title flow" when:
    - It's in the title zone
    - Its neighbors (skipping delimiters) are unknown/title tokens
    - No context delimiter separates it from those neighbors
    """
    descriptorType = Tag.LANGUAGE
    categoryType = Tag.LANGUAGE

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        # Boost LANGUAGE when neighbor tokens also have LANGUAGE possibility (metadata context)
        if (token.zone == ZONE_METADATA
                and Tag.LANGUAGE in token.possibilities):
            neighbor_lang_count = 0
            for t in tokens.loop_backward(token):
                if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                    continue
                if Tag.BRACKET in t.possibilities:
                    break
                if Tag.LANGUAGE in t.possibilities:
                    neighbor_lang_count += 1
                break
            for t in tokens.loop_forward(token):
                if Tag.DELIMITER in t.possibilities or Tag.CONTEXT_DELIMITER in t.possibilities:
                    continue
                if Tag.BRACKET in t.possibilities:
                    break
                if Tag.LANGUAGE in t.possibilities:
                    neighbor_lang_count += 1
                break
            if neighbor_lang_count > 0:
                token.add_score(Tag.LANGUAGE, 0.5 * neighbor_lang_count)

        # Only act on ambiguous labels in title zone
        if token.zone != ZONE_TITLE:
            return

        ambiguous = token.possibilities.keys() & AMBIGUOUS_IN_TITLE
        if not ambiguous:
            return

        # Check if token is in title flow: surrounded by title/unknown tokens
        # with no context delimiter between
        prev_ctx = cls._prev_meaningful(token, tokens)
        next_ctx = cls._next_meaningful(token, tokens)

        prev_is_title = (prev_ctx and (
            not prev_ctx.possibilities  # unknown
            or Tag.TITLE in prev_ctx.possibilities
            or Tag.SERIES_TITLE in prev_ctx.possibilities
        ))
        next_is_title = (next_ctx and (
            not next_ctx.possibilities
            or Tag.TITLE in next_ctx.possibilities
            or Tag.SERIES_TITLE in next_ctx.possibilities
            or Tag.SEQUENCE_NUMBER in next_ctx.possibilities  # number following title
        ))

        # Check for context delimiter between this token and neighbors
        has_context_delim_before = cls._has_context_delim_between(token, tokens, backward=True)
        has_context_delim_after = cls._has_context_delim_between(token, tokens, backward=False)

        if prev_is_title and not has_context_delim_before:
            # Token flows from title without structural break → penalize metadata
            for label in ambiguous:
                token.add_score(label, -1.5)

        if next_is_title and not has_context_delim_after:
            # Token flows into title without structural break → penalize metadata
            for label in ambiguous:
                token.add_score(label, -1.0)

    @staticmethod
    def _prev_meaningful(token: Token, tokens: Tokens):
        """Find previous non-delimiter token."""
        for t in tokens.loop_backward(token):
            if Tag.DELIMITER in t.possibilities:
                continue
            if Tag.BRACKET in t.possibilities:
                return None
            return t
        return None

    @staticmethod
    def _next_meaningful(token: Token, tokens: Tokens):
        """Find next non-delimiter token."""
        for t in tokens.loop_forward(token):
            if Tag.DELIMITER in t.possibilities:
                continue
            if Tag.BRACKET in t.possibilities:
                return None
            return t
        return None

    @staticmethod
    def _has_context_delim_between(token: Token, tokens: Tokens, backward: bool):
        """Check if there's a context delimiter between this token and its neighbor."""
        loop = tokens.loop_backward(token) if backward else tokens.loop_forward(token)
        for t in loop:
            if Tag.DELIMITER in t.possibilities:
                continue
            if Tag.CONTEXT_DELIMITER in t.possibilities:
                return True
            return False
        return False
