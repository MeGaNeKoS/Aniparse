from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token_tags import Tag
from aniparse.core.token import Tokens, Token


class EpisodeNumberScore(ScoreRule):
    descriptorType = Tag.SEQUENCE_NUMBER

    @classmethod
    def apply(cls, start_token, tokens):
        if not start_token.content.isdigit():
            return

        # If this number is part of a regex-matched video/audio term (base_score >= 1.5),
        # it's likely "8" in "8-bit" or "5.1" in "5.1ch" — reduce sequence scoring
        for alt_label in (Tag.VIDEO_TERM, Tag.AUDIO_TERM):
            poss = start_token.possibilities.get(alt_label)
            if poss and poss.score >= 1.5:
                # Still apply rules but with reduced impact — skip bracket bonus
                cls.apply_previous_token_rules(start_token, tokens)
                cls.apply_next_token_rules(start_token, tokens)
                return

        cls.apply_in_bracket_rules(start_token, tokens)
        cls.apply_previous_token_rules(start_token, tokens)
        cls.apply_next_token_rules(start_token, tokens)

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Tag.BRACKET in next_token.possibilities:
                        start_token.add_score(cls.categoryType, 0.25)
                        break
                    if Tag.DELIMITER not in next_token.possibilities:
                        break
                start_token.add_score(cls.categoryType, 0.25)
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def apply_previous_token_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                start_token.add_score(cls.categoryType, 0.25)
                break

            if (Tag.CONTEXT_DELIMITER in prev_token.possibilities
                    and Tag.SEQUENCE_RANGE not in prev_token.possibilities):
                start_token.add_score(cls.categoryType, 0.5)

            if Tag.SEQUENCE_PREFIX in prev_token.possibilities:
                start_token.add_score(cls.categoryType, 1)
                prev_token.add_score(Tag.SEQUENCE_PREFIX, 0.5)
                break  # Stop walking after finding prefix

            if Tag.TYPE in prev_token.possibilities:
                # Only boost if TYPE doesn't also have a title possibility
                if Tag.TITLE not in prev_token.possibilities:
                    start_token.add_score(cls.categoryType, 1)
                break  # Number after TYPE (e.g. "movie 02")

            if Tag.SEQUENCE_RANGE in prev_token.possibilities:
                # If this number has TITLE possibility, the range might be in the title
                # (e.g., "class 5-2") — apply reduced scoring
                title_poss = start_token.possibilities.get(Tag.TITLE)
                range_boost = 0.25 if not title_poss else 0.1
                for next_token in tokens.loop_forward(start_token):
                    if Tag.BRACKET in next_token.possibilities:
                        start_token.add_score(cls.categoryType, range_boost)

                    if Tag.CONTEXT_DELIMITER in next_token.possibilities:
                        start_token.add_score(cls.categoryType, range_boost)
                        break

                    if Tag.DELIMITER not in next_token.possibilities:
                        break
                else:
                    start_token.add_score(cls.categoryType, range_boost)
                    prev_token.add_score(Tag.SEQUENCE_RANGE, 0.5)

            if (Tag.DELIMITER not in prev_token.possibilities
                    and Tag.SEQUENCE_PREFIX not in prev_token.possibilities):
                break

    @classmethod
    def apply_next_token_rules(cls, start_token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(start_token):

            if Tag.BRACKET in next_token.possibilities:
                start_token.add_score(cls.categoryType, 0.25)
                break

            if (Tag.CONTEXT_DELIMITER in next_token.possibilities
                    and Tag.SEQUENCE_RANGE not in next_token.possibilities):
                # Reduce boost if this number is also a title candidate
                title_poss = start_token.possibilities.get(Tag.TITLE)
                boost = 0.5 if title_poss else 1
                start_token.add_score(cls.categoryType, boost)

            if Tag.SEQUENCE_RANGE in next_token.possibilities:
                for next_next_token in tokens.loop_forward(next_token):
                    if Tag.BRACKET in next_next_token.possibilities:
                        break

                    if Tag.SEQUENCE_NUMBER in next_next_token.possibilities:
                        # If the range endpoint also has TITLE possibility,
                        # this may be a title like "009-1" — reduce boost
                        title_poss = start_token.possibilities.get(Tag.TITLE)
                        end_title = next_next_token.possibilities.get(Tag.TITLE)
                        if title_poss and end_title and end_title.score >= 1.0:
                            start_token.add_score(cls.categoryType, 0.25)
                        else:
                            start_token.add_score(cls.categoryType, 1)
                            next_token.add_score(Tag.SEQUENCE_RANGE, 0.5)
                            next_next_token.add_score(Tag.SEQUENCE_NUMBER, 0.5)
                        break

                    if Tag.DELIMITER not in next_next_token.possibilities:
                        break

            if Tag.DELIMITER not in next_token.possibilities:
                break
