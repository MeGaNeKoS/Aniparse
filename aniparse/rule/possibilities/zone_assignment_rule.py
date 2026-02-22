from aniparse.core import constant
from aniparse.core.constant import (
    ZONE_TITLE, ZONE_TRANSITION, ZONE_METADATA, BASE_METADATA_LABELS,
)
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag

METADATA_LABELS = BASE_METADATA_LABELS | {
    Tag.RELEASE_INFORMATION, Tag.RELEASE_VERSION_PREFIX, Tag.EXTRA_INFO,
}


class ZoneAssignmentPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        tokens = parser.tokens.tokens

        # Pass 1: assign zones
        zone = ZONE_TITLE
        depth = 0
        seen_non_bracket = False  # have we seen any non-bracket content yet?
        zone_stack = []  # save zone before entering brackets

        for i, token in enumerate(tokens):
            c = token.content

            if c in constant.OPEN_BRACKETS:
                token.zone = ZONE_TRANSITION
                zone_stack.append(zone)
                depth += 1
                continue
            if c in constant.CLOSE_BRACKETS:
                token.zone = ZONE_TRANSITION
                depth -= 1
                if depth <= 0:
                    depth = 0
                    # Restore pre-bracket zone
                    zone = zone_stack.pop() if zone_stack else ZONE_TITLE
                    # If we haven't seen non-bracket content yet, stay in title zone
                    if not seen_non_bracket:
                        zone = ZONE_TITLE
                continue

            if depth > 0:
                token.zone = ZONE_METADATA
                continue

            # Track that we've seen non-bracket content
            if not (len(c) == 1 and c in constant.DELIMITERS):
                seen_non_bracket = True

            # Context delimiter — check if followed by metadata
            if Tag.CONTEXT_DELIMITER in token.possibilities:
                if cls._followed_by_metadata(tokens, i):
                    token.zone = ZONE_TRANSITION
                    zone = ZONE_METADATA
                elif zone == ZONE_TITLE and cls._followed_by_comma_list(tokens, i):
                    token.zone = ZONE_TRANSITION
                    zone = ZONE_METADATA
                else:
                    token.zone = zone  # title-internal dash
                continue

            # SEQUENCE_PREFIX + number → structural boundary
            if Tag.SEQUENCE_PREFIX in token.possibilities and cls._has_following_number(tokens, i):
                token.zone = ZONE_METADATA
                zone = ZONE_METADATA
                continue

            token.zone = zone

        # Pass 2: clean up possibilities based on zones
        for i, token in enumerate(tokens):
            # TYPE/SEQUENCE_PREFIX followed by number → boost to beat LANGUAGE
            if (Tag.LANGUAGE in token.possibilities
                    and (Tag.SEQUENCE_PREFIX in token.possibilities
                         or Tag.TYPE in token.possibilities)
                    and cls._has_following_number(tokens, i)):
                if Tag.SEQUENCE_PREFIX in token.possibilities:
                    token.add_score(Tag.SEQUENCE_PREFIX, 1.0)
                if Tag.TYPE in token.possibilities:
                    token.add_score(Tag.TYPE, 1.0)
            # SEQUENCE_PREFIX without following number → remove prefix
            # But only for season/episode/volume prefixes, not content types (e.g. "clean ending")
            if (token.zone in (ZONE_TITLE, ZONE_METADATA)
                    and Tag.SEQUENCE_PREFIX in token.possibilities
                    and not cls._has_following_number(tokens, i)):
                poss = token.possibilities[Tag.SEQUENCE_PREFIX]
                if poss.descriptor in (Tag.SEASON, Tag.EPISODE, Tag.VOLUME):
                    token.remove_possibility(Tag.SEQUENCE_PREFIX)

            # RELEASE_INFORMATION in title zone → remove unless preceded by number
            # or confirmed by regex (score >= 1.5)
            if (token.zone == ZONE_TITLE
                    and Tag.RELEASE_INFORMATION in token.possibilities):
                if (not cls._preceded_by_number(tokens, i)
                        and token.possibilities[Tag.RELEASE_INFORMATION].score < 1.5):
                    token.remove_possibility(Tag.RELEASE_INFORMATION)

    @staticmethod
    def _followed_by_metadata(tokens, idx):
        """Check if tokens after idx (skipping delimiters) start with metadata."""
        for j in range(idx + 1, len(tokens)):
            t = tokens[j]
            if len(t.content) == 1 and t.content in constant.DELIMITERS:
                continue
            # Brackets count as metadata boundary
            if t.content in constant.OPEN_BRACKETS:
                return True
            # Check for SEQUENCE_PREFIX — content types count as metadata directly
            if Tag.SEQUENCE_PREFIX in t.possibilities:
                poss = t.possibilities[Tag.SEQUENCE_PREFIX]
                if poss.descriptor in (Tag.CONTENT_TYPE, Tag.CONTENT_IDENTIFIER):
                    return True
                # Season/episode/volume need a following number
                for k in range(j + 1, len(tokens)):
                    t2 = tokens[k]
                    if len(t2.content) == 1 and t2.content in constant.DELIMITERS:
                        continue
                    return Tag.SEQUENCE_NUMBER in t2.possibilities
                return False
            # Bare SEQUENCE_NUMBER
            if Tag.SEQUENCE_NUMBER in t.possibilities:
                return True
            # Any metadata label
            for label in t.possibilities:
                if label in METADATA_LABELS:
                    return True
            return False
        return False

    @staticmethod
    def _has_following_number(tokens, idx):
        """Check if token at idx is followed by a SEQUENCE_NUMBER (skipping delimiters).
        Returns False if the number is more likely a VIDEO_RESOLUTION."""
        for j in range(idx + 1, len(tokens)):
            t = tokens[j]
            if len(t.content) == 1 and t.content in constant.DELIMITERS:
                continue
            if Tag.SEQUENCE_NUMBER not in t.possibilities:
                return False
            # If VIDEO_RESOLUTION is at least as strong, this isn't an episode number
            vr = t.possibilities.get(Tag.VIDEO_RESOLUTION)
            sn = t.possibilities.get(Tag.SEQUENCE_NUMBER)
            if vr and sn and vr.score >= sn.score:
                return False
            return True
        return False

    @staticmethod
    def _followed_by_comma_list(tokens, idx):
        """Check if text after idx contains commas before the next context delimiter or bracket."""
        comma_count = 0
        word_count = 0
        for j in range(idx + 1, len(tokens)):
            t = tokens[j]
            if t.content in constant.OPEN_BRACKETS or t.content in constant.CLOSE_BRACKETS:
                break
            if (Tag.CONTEXT_DELIMITER in t.possibilities
                    and Tag.DELIMITER not in t.possibilities):
                break  # hit a structural dash
            if t.content == constant.COMMA:
                comma_count += 1
            elif len(t.content) > 1 and t.content.isalpha():
                word_count += 1
        return comma_count >= 2 and word_count >= 3

    @staticmethod
    def _preceded_by_number(tokens, idx):
        """Check if token at idx is preceded by a number (skipping delimiters)."""
        for j in range(idx - 1, -1, -1):
            t = tokens[j]
            if len(t.content) == 1 and t.content in constant.DELIMITERS:
                continue
            return t.content.isdigit()
        return False
