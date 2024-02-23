from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.element import Label
from aniparse.token import Tokens, Token


class EpisodeNumberScore(ScoreRule):
    descriptorType = Label.SEQUENCE_NUMBER

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
            if Label.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Label.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType] += 0.25
                        break
                    if Label.DELIMITER not in next_token.possibilities:
                        break
                start_token.possibilities[cls.descriptorType] += 0.25
                break
            if Label.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def apply_previous_token_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Label.BRACKET in prev_token.possibilities:
                start_token.possibilities[cls.descriptorType] += 0.25
                break

            if (Label.CONTEXT_DELIMITER in prev_token.possibilities
                    and Label.SEQUENCE_RANGE not in prev_token.possibilities):
                start_token.possibilities[cls.descriptorType] += 0.5

            if Label.SEQUENCE_PREFIX in prev_token.possibilities:
                start_token.possibilities[cls.descriptorType] += 1
                prev_token.possibilities[Label.SEQUENCE_PREFIX] += 0.5

            if Label.SEQUENCE_RANGE in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Label.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType] += 0.25

                    if Label.CONTEXT_DELIMITER in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType] += 0.25
                        break

                    if Label.DELIMITER not in next_token.possibilities:
                        break
                else:
                    start_token.possibilities[cls.descriptorType] += 0.25
                    prev_token.possibilities[Label.SEQUENCE_RANGE] += 0.5

            if (Label.DELIMITER not in prev_token.possibilities
                    and Label.SEQUENCE_PREFIX not in prev_token.possibilities):
                break

    @classmethod
    def apply_next_token_rules(cls, start_token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(start_token):

            if Label.BRACKET in next_token.possibilities:
                start_token.possibilities[cls.descriptorType] += 0.25
                break

            if (Label.CONTEXT_DELIMITER in next_token.possibilities
                    and Label.SEQUENCE_RANGE not in next_token.possibilities):
                start_token.possibilities[cls.descriptorType] += 1

            if Label.SEQUENCE_RANGE in next_token.possibilities:
                for next_next_token in tokens.loop_forward(next_token):
                    if Label.BRACKET in next_token.possibilities:
                        break

                    if Label.SEQUENCE_NUMBER in next_next_token.possibilities:
                        start_token.possibilities[cls.descriptorType] += 1
                        next_token.possibilities[Label.SEQUENCE_RANGE] += 0.5
                        next_next_token.possibilities[Label.SEQUENCE_NUMBER] += 0.5
                    if Label.SEQUENCE_NUMBER in next_next_token.possibilities:
                        next_next_token.possibilities[Label.SEQUENCE_NUMBER] += 0.5

                    if Label.DELIMITER not in next_token.possibilities:
                        break

            if Label.DELIMITER not in next_token.possibilities:
                break

