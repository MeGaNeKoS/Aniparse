from typing import Iterator, Tuple

from aniparse.token import Tokens, Token
import re

MIXED_TOKEN_REGEX = re.compile(
    r"[a-z][A-Z]+"  # Inverted Case words: lowercase followed by uppercase
    r"|[A-Z]?[a-z]+"  # Words starting with an optional uppercase followed by lowercase letters
    r"|[A-Z]+"  # Uppercase sequences
    r"|\d+"  # Sequences of digits
    r"|[^a-zA-Z\d]",  # Non-alphanumeric characters
)

# test_regex = """Properly CamelCased UPPER alphanum12345 !@# not_A_word Num456 otherTest cAMELcASE 789 ! cASED but
# [夜莺家族][樱桃小丸子第二期(Chibi Maruko-chan II)][1401]小玉想飞上天&樱家中彩票了[2023.09.10][GB_JP][1080P][MP4]"""


class Tokenizer:
    def __init__(self, filename: str):
        """
        Initialize a Tokenizer object.

        Parameters:
            filename (str): The string representing the filename to be tokenized.
        """
        self.filename = filename
        self.tokens = Tokens()

    def tokenize(self) -> Tokens:
        for content, start_post in self.generate_tokens():
            self.tokens.add_token(Token(content=content, index=start_post))
        return self.tokens

    def generate_tokens(self) -> Iterator[Tuple[str, int]]:
        for match in MIXED_TOKEN_REGEX.finditer(self.filename):
            token_string = match.group(0)
            start_index = match.start()
            yield token_string, start_index
