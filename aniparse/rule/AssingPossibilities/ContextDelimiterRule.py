from aniparse.abstraction.ParserBase import PossibilityRule
from aniparse.element import DescriptorType
from aniparse.parser import BaseParser


class ContextDelimiterPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: BaseParser):
        for token in parser.tokens:
            if DescriptorType.CONTEXT_DELIMITER not in token.possibilities:
                continue

            if DescriptorType.DELIMITER in token.possibilities:
                prev_token = parser.tokens.find_prev(token)
                next_token = parser.tokens.find_next(token)

                if prev_token and next_token:
                    if (DescriptorType.DELIMITER in prev_token.possibilities and
                            DescriptorType.DELIMITER in next_token.possibilities):
                        token.remove_possibility(DescriptorType.DELIMITER)
