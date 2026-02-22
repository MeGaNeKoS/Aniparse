from aniparse.core.token import Tokens
from aniparse.core.token_tags import Tag
from aniparse.core.constant import BRACKETS


def resolve(tokens: Tokens) -> None:
    """Pick winning possibility per token, set token._category to winner."""
    for token in tokens:
        if not token.possibilities:
            continue
        best = token.get_best_possibility()
        if best is not None:
            label, possibility = best

            # Tiebreaker: regex-matched metadata beats SEQUENCE_NUMBER.
            if label == Tag.SEQUENCE_NUMBER:
                for alt_label in (Tag.YEAR, Tag.VIDEO_TERM, Tag.AUDIO_TERM, Tag.VIDEO_RESOLUTION):
                    alt = token.possibilities.get(alt_label)
                    if alt and (alt.element is not None or alt_label == Tag.AUDIO_TERM) and alt.score >= 1.5:
                        label, possibility = alt_label, alt
                        break

            # Tiebreaker: RELEASE_GROUP with element beats SEQUENCE_NUMBER
            if label == Tag.SEQUENCE_NUMBER:
                alt = token.possibilities.get(Tag.RELEASE_GROUP)
                if alt and alt.element is not None:
                    label, possibility = Tag.RELEASE_GROUP, alt

            # Tiebreaker: keyword-matched SEQUENCE_PREFIX should beat
            # SEQUENCE_NUMBER on non-digit tokens
            if label == Tag.SEQUENCE_NUMBER and not token.content.isdigit():
                alt = token.possibilities.get(Tag.SEQUENCE_PREFIX)
                if alt and alt.element is not None:
                    label, possibility = Tag.SEQUENCE_PREFIX, alt

            # Tiebreaker: TITLE should beat SEQUENCE_NUMBER only when TITLE
            # has significantly higher score
            if label == Tag.SEQUENCE_NUMBER:
                alt = token.possibilities.get(Tag.TITLE)
                if alt and alt.score > possibility.score + 0.5:
                    label, possibility = Tag.TITLE, alt

            # Tiebreaker: regex-matched VIDEO_TERM/AUDIO_TERM beats SEQUENCE_PREFIX
            if label == Tag.SEQUENCE_PREFIX:
                for alt_label in (Tag.VIDEO_TERM, Tag.AUDIO_TERM):
                    alt = token.possibilities.get(alt_label)
                    if alt and alt.element is not None and alt.score >= possibility.score:
                        label, possibility = alt_label, alt
                        break

            # Tiebreaker: TITLE beats SEQUENCE_RANGE when scores are equal
            if label == Tag.SEQUENCE_RANGE:
                alt = token.possibilities.get(Tag.TITLE)
                if alt and alt.score >= possibility.score:
                    label, possibility = Tag.TITLE, alt

            # Tiebreaker: BRACKET always wins for actual bracket characters
            # unless TITLE or RELEASE_GROUP has higher score
            if label != Tag.BRACKET and Tag.BRACKET in token.possibilities:
                if token.content in BRACKETS:
                    title_poss = token.possibilities.get(Tag.TITLE)
                    rg_poss = token.possibilities.get(Tag.RELEASE_GROUP)
                    has_override = ((title_poss and title_poss.score > 0)
                                    or (rg_poss and rg_poss.score > 0))
                    if not has_override:
                        label = Tag.BRACKET

            token._category = label


def calculate_confidence(tokens: Tokens) -> float:
    """Average margin between winner and runner-up across resolved tokens."""
    margins = []
    for token in tokens:
        if not token.possibilities or len(token.possibilities) < 1:
            continue
        scores = sorted((p.score for p in token.possibilities.values()), reverse=True)
        winner = scores[0]
        runner_up = scores[1] if len(scores) > 1 else 0.0
        margins.append(winner - runner_up)
    if not margins:
        return 0.0
    return sum(margins) / len(margins)
