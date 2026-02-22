from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token_tags import Tag
from aniparse.core.token import Tokens, Token


class SeriesYearScore(ScoreRule):
    descriptorType = Tag.SERIES_YEAR

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        if not token.content.isdigit():
            return
        # Year range is already gated by NumberRule/YearRule via config;
        # if SERIES_YEAR possibility exists, the value is in range.
        token.add_score(cls.categoryType, 1.0)
        cls.apply_in_bracket_rules(token, tokens)
        cls.between_context_delimiter(token, tokens)
        cls.apply_alone_in_brackets(token, tokens)

    @classmethod
    def apply_alone_in_brackets(cls, start_token: Token, tokens: Tokens):
        """Strong bonus when a year-range number is alone in brackets, e.g. (1994)."""
        # Check backward: only delimiters until bracket
        found_open = False
        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                found_open = True
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                return
        if not found_open:
            return
        # Check forward: only delimiters until bracket
        for next_token in tokens.loop_forward(start_token):
            if Tag.BRACKET in next_token.possibilities:
                start_token.add_score(cls.categoryType, 1.5)
                return
            if Tag.DELIMITER not in next_token.possibilities:
                return

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Tag.BRACKET in next_token.possibilities:
                        start_token.add_score(cls.categoryType, 0.5)
                        break
                    if Tag.DELIMITER not in next_token.possibilities:
                        break
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def between_context_delimiter(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Tag.CONTEXT_DELIMITER in prev_token.possibilities:
                start_token.add_score(cls.categoryType, 0.5)
            if Tag.DELIMITER not in prev_token.possibilities:
                break
        for next_token in tokens.loop_forward(start_token):
            if Tag.CONTEXT_DELIMITER in next_token.possibilities:
                start_token.add_score(cls.categoryType, 0.5)
            if Tag.DELIMITER not in next_token.possibilities:
                break
