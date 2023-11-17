from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.element import DescriptorType
from aniparse.token import Tokens, Token


class EpisodeNumberScoreP(ScoreRule):
    descriptorType = DescriptorType.EPISODE_NUMBER

    @classmethod
    def apply(cls, token, tokens):
        if not token.content.isdigit():
            return

        # Season 1, Episode 1
        cls.apply_previous_token_rules(token, tokens)
        # 1 of 12, 1-12
        cls.apply_next_token_rules(token, tokens)
        cls.apply_multi_episode_rules(token, tokens)
        cls.apply_season_episode_format_rules(token, tokens)

    @classmethod
    def apply_previous_token_rules(cls, token: Token, tokens: Tokens):

        for prev_token in tokens.loop_backward(token):

            if DescriptorType.BRACKET in prev_token.possibilities:
                break

            if DescriptorType.CONTEXT_DELIMITER in prev_token.possibilities:
                token.possibilities[cls.descriptorType] += 0.5
                break

            if DescriptorType.SEASON_PREFIX in prev_token.possibilities:
                token.possibilities[cls.descriptorType] -= 1

            if DescriptorType.EPISODE_PREFIX in prev_token.possibilities:
                token.possibilities[cls.descriptorType] += 1
                prev_token.possibilities[DescriptorType.EPISODE_PREFIX] += 0.5

            if DescriptorType.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def apply_next_token_rules(cls, token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(token):

            if DescriptorType.BRACKET in next_token.possibilities:
                break

            if DescriptorType.CONTEXT_DELIMITER in next_token.possibilities:
                token.possibilities[cls.descriptorType] += 0.5
                break

            if DescriptorType.EPISODE_RANGE in next_token.possibilities:
                cls.apply_next_next_token_rules(token, tokens, next_token)

            if DescriptorType.DELIMITER not in next_token.possibilities:
                break

    @classmethod
    def apply_next_next_token_rules(cls, token: Token, tokens: Tokens, next_token: Token):
        for next_next_token in tokens.loop_forward(next_token):
            if DescriptorType.BRACKET in next_token.possibilities:
                break

            if DescriptorType.EPISODE_TOTAL in next_next_token.possibilities:
                token.possibilities[cls.descriptorType] += 1
                next_token.possibilities[DescriptorType.EPISODE_RANGE] += 0.5
                next_next_token.possibilities[DescriptorType.EPISODE_TOTAL] += 0.5
            if DescriptorType.EPISODE_NUMBER in next_next_token.possibilities:
                next_next_token.possibilities[DescriptorType.EPISODE_NUMBER] += 0.5

            if DescriptorType.DELIMITER not in next_token.possibilities:
                break

    @classmethod
    def apply_multi_episode_rules(cls, token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(token):

            if DescriptorType.EPISODE_RANGE in next_token.possibilities:
                for next_next_token in tokens.loop_forward(next_token):
                    if next_next_token.content.isdigit():
                        token.possibilities[cls.descriptorType] += 1
                        next_token.possibilities[DescriptorType.EPISODE_RANGE] += 0.5

                        if DescriptorType.EPISODE_TOTAL in next_next_token.possibilities:
                            next_next_token.possibilities[DescriptorType.EPISODE_TOTAL] += 0.5
                        if DescriptorType.EPISODE_NUMBER in next_next_token.possibilities:
                            next_next_token.possibilities[DescriptorType.EPISODE_NUMBER] += 0.5
                        break

                    if DescriptorType.DELIMITER not in next_next_token.possibilities:
                        break

            if DescriptorType.DELIMITER not in next_token.possibilities:
                break

    @classmethod
    def apply_season_episode_format_rules(cls, token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(token):

            if DescriptorType.DELIMITER in prev_token.possibilities:
                break

            if DescriptorType.SEASON_NUMBER in prev_token.possibilities:
                token.possibilities[cls.descriptorType] += 1
                break
