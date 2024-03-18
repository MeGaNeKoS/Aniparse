from aniparse.abstraction.ParserBase import PossibilityRule
from aniparse.token_tags import Category, Descriptor
from aniparse.parser import BaseParser


class ContextDelimiterPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: BaseParser):
        for token in parser.tokens:
            if Category.CONTEXT_DELIMITER not in token.possibilities and Category.DELIMITER not in token.possibilities:
                continue

            if Category.DELIMITER in token.possibilities:
                prev_token = parser.tokens.find_prev(token)
                next_token = parser.tokens.find_next(token)

                if prev_token and next_token:
                    if (Category.DELIMITER in prev_token.possibilities and
                            Category.DELIMITER in next_token.possibilities and
                            prev_token.content == next_token.content != token.content):
                        token.remove_possibility(Category.DELIMITER)
                        token.add_possibility(Descriptor.CONTEXT_DELIMITER)
