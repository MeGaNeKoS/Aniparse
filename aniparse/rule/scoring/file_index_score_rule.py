from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token_tags import Tag
from aniparse.core.token import Token, Tokens


class FileIndexRule(ScoreRule):
    descriptorType = Tag.FILE_INDEX

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        if not token.content.isdigit():
            return

        cls.apply_previous_token_rules(token, tokens)
        cls.apply_next_token_rules(token, tokens)

    @classmethod
    def apply_previous_token_rules(cls, token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(token):
            if Tag.BRACKET in prev_token.possibilities:
                continue
            if Tag.CONTEXT_DELIMITER in prev_token.possibilities:
                continue
            if Tag.DELIMITER in prev_token.possibilities:
                continue
            break
        else:
            last_delimiter = None
            first_next_token = None
            second_next_token = None
            same_delimiter_in_a_row = False

            for next_token in tokens.loop_forward(token):
                if not first_next_token:
                    first_next_token = next_token
                    if Tag.DELIMITER in next_token.possibilities:
                        last_delimiter = next_token.content
                    continue

                if Tag.DELIMITER in next_token.possibilities:
                    if next_token.content == last_delimiter:
                        same_delimiter_in_a_row = True
                    else:
                        token.add_score(cls.categoryType, 0.5)
                        last_delimiter = next_token.content
                        same_delimiter_in_a_row = False
                else:
                    if same_delimiter_in_a_row:
                        token.add_score(cls.categoryType, 0.25)

                if not second_next_token:
                    second_next_token = next_token
                    if Tag.BRACKET in next_token.possibilities:
                        token.add_score(cls.categoryType, 0.5)
                        break
                    if Tag.CONTEXT_DELIMITER in next_token.possibilities:
                        token.add_score(cls.categoryType, 0.25)
                        last_delimiter = next_token.content
                    continue

                if Tag.DELIMITER not in next_token.possibilities:
                    break

    @classmethod
    def apply_next_token_rules(cls, token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(token):
            if Tag.BRACKET in next_token.possibilities:
                continue
            if Tag.CONTEXT_DELIMITER in next_token.possibilities:
                continue
            if Tag.DELIMITER in next_token.possibilities:
                continue
            break
        else:
            last_delimiter = None
            first_prev_token = None
            second_prev_token = None
            same_delimiter_in_a_row = False
            for prev_token in tokens.loop_backward(token):
                if not first_prev_token:
                    first_prev_token = prev_token
                    if Tag.DELIMITER in prev_token.possibilities:
                        last_delimiter = prev_token.content
                    continue

                if Tag.DELIMITER in prev_token.possibilities:
                    if prev_token.content == last_delimiter:
                        same_delimiter_in_a_row = True
                    else:
                        token.add_score(cls.categoryType, 0.25)
                        last_delimiter = prev_token.content
                        same_delimiter_in_a_row = False
                    continue
                else:
                    if same_delimiter_in_a_row:
                        token.add_score(cls.categoryType, 0.25)

                if not second_prev_token:
                    second_prev_token = prev_token
                    if Tag.BRACKET in prev_token.possibilities:
                        token.add_score(cls.categoryType, 0.5)
                        break
                    if Tag.CONTEXT_DELIMITER in prev_token.possibilities:
                        token.add_score(cls.categoryType, 0.25)
                        last_delimiter = prev_token.content
                    continue

                if Tag.DELIMITER not in prev_token.possibilities:
                    break
