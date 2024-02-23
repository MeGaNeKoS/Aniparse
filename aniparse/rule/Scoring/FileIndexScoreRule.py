from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.element import Label
from aniparse.token import Token, Tokens


class FileIndexRule(ScoreRule):
    descriptorType = Label.FILE_INDEX

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        if not token.content.isdigit():
            return

        cls.apply_previous_token_rules(token, tokens)
        cls.apply_next_token_rules(token, tokens)

    @classmethod
    def apply_previous_token_rules(cls, token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(token):
            if Label.BRACKET in prev_token.possibilities:
                continue
            if Label.CONTEXT_DELIMITER in prev_token.possibilities:
                continue
            if Label.DELIMITER in prev_token.possibilities:
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
                    if Label.DELIMITER in next_token.possibilities:
                        last_delimiter = next_token.content
                    continue

                # Check if the current token is a delimiter and matches the last delimiter seen
                if Label.DELIMITER in next_token.possibilities:
                    if next_token.content == last_delimiter:
                        # Two same delimiters in a row might not indicate a file index directly
                        same_delimiter_in_a_row = True
                    else:
                        # Different delimiters suggest a higher likelihood of a file index
                        token.possibilities[cls.descriptorType] += 0.5
                        last_delimiter = next_token.content  # Update last delimiter for further comparison
                        same_delimiter_in_a_row = False  # Reset for next iteration
                else:
                    if same_delimiter_in_a_row:
                        # If the previous condition was two delimiters in a row, adjust score slightly
                        token.possibilities[cls.descriptorType] += 0.25

                if not second_next_token:
                    second_next_token = next_token
                    if Label.BRACKET in next_token.possibilities:
                        # Presence of a bracket may indicate a file index, especially following numeric tokens
                        token.possibilities[cls.descriptorType] += 0.5
                        break
                    if Label.CONTEXT_DELIMITER in next_token.possibilities:
                        token.possibilities[cls.descriptorType] += 0.25
                        last_delimiter = next_token.content
                    continue

                # Reset the delimiter sequence flag if the next token is not a delimiter
                if Label.DELIMITER not in next_token.possibilities:
                    same_delimiter_in_a_row = False
                    break

    @classmethod
    def apply_next_token_rules(cls, token: Token, tokens: Tokens):
        for next_token in tokens.loop_forward(token):
            if Label.BRACKET in next_token.possibilities:
                continue
            if Label.CONTEXT_DELIMITER in next_token.possibilities:
                continue
            if Label.DELIMITER in next_token.possibilities:
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
                    if Label.DELIMITER in prev_token.possibilities:
                        last_delimiter = prev_token.content
                    continue

                if Label.DELIMITER in prev_token.possibilities:
                    if prev_token.content == last_delimiter:
                        same_delimiter_in_a_row = True
                    else:
                        token.possibilities[cls.descriptorType] += 0.25
                        last_delimiter = prev_token.content
                    continue
                else:
                    if same_delimiter_in_a_row:
                        # If the previous condition was two delimiters in a row, adjust score slightly
                        token.possibilities[cls.descriptorType] += 0.25

                if not second_prev_token:
                    second_prev_token = prev_token
                    if Label.BRACKET in prev_token.possibilities:
                        token.possibilities[cls.descriptorType] += 0.5
                        break
                    if Label.CONTEXT_DELIMITER in prev_token.possibilities:
                        token.possibilities[cls.descriptorType] += 0.25
                        last_delimiter = prev_token.content
                    continue

                if Label.DELIMITER not in prev_token.possibilities:
                    same_delimiter_in_a_row = False
                    break
