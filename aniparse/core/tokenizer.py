import re
from typing import Iterator, Tuple

from aniparse.wordlist import WordListManager
from aniparse.core.token import Tokens, Token

_L = r"a-zA-Z\u00C0-\u024F\u1E00-\u1EFF"  # ASCII + Latin Extended + Latin Additional
_CJK = r"\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uF900-\uFAFF"  # CJK + Hiragana + Katakana
MIXED_TOKEN_REGEX = re.compile(
    r"\d+(?:st|nd|rd|th)"  # ordinals: 1st, 2nd, 3rd, 4th
    rf"|[{_CJK}]+"  # CJK/Japanese character sequences
    rf"|[a-z\u00E0-\u024F\u1E00-\u1EFF][A-Z\u00C0-\u024F\u1E00-\u1EFF]+"
    rf"|[A-Z\u00C0-\u024F\u1E00-\u1EFF]?[a-z\u00E0-\u024F\u1E00-\u1EFF]+"
    rf"|[A-Z\u00C0-\u024F\u1E00-\u1EFF]+"
    r"|\d+"
    rf"|[^{_L}{_CJK}\d]",
)


class Tokenizer:

    def __init__(self, filename: str, wordlist_manager: WordListManager):
        self.filename = filename
        self.wordlist_manager = wordlist_manager
        self.tokens = Tokens()

    def tokenize(self) -> Tokens:
        for content, start_pos in self.generate_tokens():
            self.tokens.add_token(Token(content=content, index=start_pos))
        return self.tokens

    def generate_tokens(self) -> Iterator[Tuple[str, int]]:
        for match in MIXED_TOKEN_REGEX.finditer(self.filename):
            token_string = match.group(0)
            start_index = match.start()
            yield token_string, start_index
