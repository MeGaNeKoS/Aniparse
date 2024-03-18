from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.token_tags import Category
from aniparse.token import Token, Tokens


class VideoTermScoreRule(ScoreRule):
    descriptorType = Category.VIDEO_TERM

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        cls.apply_in_bracket_rules(token, tokens)
        cls.check_neighbor_token(token, tokens)

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.FILE_CHECKSUM in prev_token.possibilities:
                continue
            if Category.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Category.FILE_CHECKSUM in next_token.possibilities:
                        continue
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
    def check_neighbor_token(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if Category.FILE_CHECKSUM in prev_token.possibilities:
                continue
            flag = False
            for possibility in prev_token.possibilities:
                if possibility in Category.get_optional_info():
                    if possibility == cls.descriptorType:
                        continue
                    prev_token.possibilities[possibility]["score"] += 0.25
                    flag = True
            if flag:
                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break

            if Category.DELIMITER not in prev_token.possibilities:
                break

        for next_token in tokens.loop_forward(start_token):
            if Category.FILE_CHECKSUM in next_token.possibilities:
                continue
            flag = False
            for possibility in next_token.possibilities:
                if possibility in Category.get_optional_info():
                    next_token.possibilities[possibility]["score"] += 0.25
                    flag = True
            if flag:
                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break

            if Category.DELIMITER not in next_token.possibilities:
                break
