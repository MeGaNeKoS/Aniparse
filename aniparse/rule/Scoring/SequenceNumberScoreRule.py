from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.token_tags import Category
from aniparse.token import Tokens, Token


class EpisodeNumberScore(ScoreRule):
    descriptorType = Category.SEQUENCE_NUMBER

    @classmethod
    def apply(cls, start_token, tokens):
        if not start_token.content.isdigit():
            return

        # Season 1, Episode 1
        cls.apply_in_bracket_rules(start_token, tokens)
        cls.apply_previous_token_rules(start_token, tokens)
        # 1 of 12, 1-12
        cls.apply_next_token_rules(start_token, tokens)

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Category.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 0.25
                        break
                    if Category.DELIMITER not in next_token.possibilities:
                        break
                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break
            if Category.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def apply_previous_token_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.BRACKET in prev_token.possibilities:
                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break

            if (Category.CONTEXT_DELIMITER in prev_token.possibilities
                    and Category.SEQUENCE_RANGE not in prev_token.possibilities):
                start_token.possibilities[cls.descriptorType]["score"] += 0.5

            if Category.SEQUENCE_PREFIX in prev_token.possibilities:
                start_token.possibilities[cls.descriptorType]["score"] += 1
                prev_token.possibilities[Category.SEQUENCE_PREFIX]["score"] += 0.5

            if Category.SEQUENCE_RANGE in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Category.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 0.25

                    if Category.CONTEXT_DELIMITER in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 0.25
                        break

                    if Category.DELIMITER not in next_token.possibilities:
                        break
                else:
                    start_token.possibilities[cls.descriptorType]["score"] += 0.25
                    prev_token.possibilities[Category.SEQUENCE_RANGE]["score"] += 0.5

            if (Category.DELIMITER not in prev_token.possibilities
                    and Category.SEQUENCE_PREFIX not in prev_token.possibilities):
                break

    @classmethod
    def apply_next_token_rules(cls, start_token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(start_token):

            if Category.BRACKET in next_token.possibilities:
                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break

            if (Category.CONTEXT_DELIMITER in next_token.possibilities
                    and Category.SEQUENCE_RANGE not in next_token.possibilities):
                start_token.possibilities[cls.descriptorType]["score"] += 1

            if Category.SEQUENCE_RANGE in next_token.possibilities:
                for next_next_token in tokens.loop_forward(next_token):
                    if Category.BRACKET in next_token.possibilities:
                        break

                    if Category.SEQUENCE_NUMBER in next_next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 1
                        next_token.possibilities[Category.SEQUENCE_RANGE]["score"] += 0.5
                        next_next_token.possibilities[Category.SEQUENCE_NUMBER]["score"] += 0.5
                    if Category.SEQUENCE_NUMBER in next_next_token.possibilities:
                        next_next_token.possibilities[Category.SEQUENCE_NUMBER]["score"] += 0.5

                    if Category.DELIMITER not in next_token.possibilities:
                        break

            if Category.DELIMITER not in next_token.possibilities:
                break

