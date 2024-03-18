from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.token_tags import Category
from aniparse.token import Tokens, Token


class SeriesYearScore(ScoreRule):
    descriptorType = Category.YEAR

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        cls.apply_in_bracket_rules(token, tokens)
        cls.between_context_delimiter(token, tokens)

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Category.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 0.5
                        break
                    if Category.DELIMITER not in next_token.possibilities:
                        break
                break
            if Category.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def between_context_delimiter(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.CONTEXT_DELIMITER in prev_token.possibilities:
                start_token.possibilities[cls.descriptorType]["score"] += 0.5

            if Category.DELIMITER not in prev_token.possibilities:
                break
        for next_token in tokens.loop_forward(start_token):
            if Category.CONTEXT_DELIMITER in next_token.possibilities:
                start_token.possibilities[cls.descriptorType]["score"] += 0.5

            if Category.DELIMITER not in next_token.possibilities:
                break
