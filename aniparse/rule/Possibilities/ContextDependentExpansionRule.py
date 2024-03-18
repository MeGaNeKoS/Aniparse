from typing import Union

from aniparse import constant
from aniparse.abstraction.ParserBase import PossibilityRule, AbstractParser
from aniparse.token_tags import Category, Descriptor
from aniparse.token import Token


class ContextDependentExpansionPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        for token in parser.tokens:
            if not token or not token.content:
                continue

            # Check if the token is marked as context-dependent
            if Category.CONTEXT_DEPENDENT not in token.possibilities:
                continue

            if token.content.upper() in constant.DISAMBIGUATION_WORDS:
                cls.handle_disambiguation_word(parser, token)

            if token.content.upper() in constant.DELIMITERS:
                token.remove_possibility(Category.CONTEXT_DEPENDENT)
                token.add_possibility([
                    Descriptor.DELIMITER
                ])

            if token.content.upper() in ["+", "&"]:
                cls.handle_plus(parser, token)

    @classmethod
    def handle_plus(cls, parser: AbstractParser, token: Token):
        prev_token = cls.get_previous_relevant_token(parser, token)

        next_token = cls.get_next_relevant_token(parser, token)

        if prev_token and next_token:
            for category, descriptors in prev_token.possibilities.items():
                if not next_token.content.isdigit() and category in [
                    Category.SEQUENCE_NUMBER,
                    Category.SEQUENCE_NUMBER,
                    Category.SEQUENCE_NUMBER,
                ]:
                    continue
                next_token.add_possibility(descriptors["descriptor"])

    @classmethod
    def handle_disambiguation_word(cls, parser: AbstractParser, token: Token):
        word = token.content.upper()
        next_token = cls.get_next_relevant_token(parser, token)

        if word == "THE" and next_token and next_token.content.upper() in {'END', 'FINAL', "MOVIE", "MOVIES"}:
            token.remove_possibility(Category.CONTEXT_DEPENDENT)
            next_token.remove_possibility()
            next_token.add_possibility([pos["descriptor"] for pos in token.possibilities.values()])

        elif word == "PART" and next_token and next_token.content.isdigit():
            token.remove_possibility(Category.CONTEXT_DEPENDENT)
            next_token.remove_possibility()
            next_token.add_possibility([pos["descriptor"] for pos in token.possibilities.values()])

    @staticmethod
    def get_next_relevant_token(parser: AbstractParser, current_token: Token) -> Union[Token, None]:
        for next_token in parser.tokens.loop_forward(current_token):
            if next_token.content in constant.DELIMITERS or next_token.content in constant.BRACKETS:
                continue
            return next_token
        return None

    @staticmethod
    def get_previous_relevant_token(parser, current_token) -> Union[Token, None]:
        for prev_token in parser.tokens.loop_backward(current_token):
            if prev_token.content in constant.DELIMITERS or prev_token.content in constant.BRACKETS:
                continue
            return prev_token
        return None
