from typing import Union

from aniparse.core import constant
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag
from aniparse.core.token import Token


class ContextDependentExpansionPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        for token in parser.tokens:
            if not token or not token.content:
                continue

            if Tag.CONTEXT_DEPENDENT not in token.possibilities:
                continue

            word = token.content.upper()

            # Range connectors (+ and &) — propagate prev possibilities to next token
            if word in parser.config.range_connectors:
                cls.handle_plus(parser, token)
                continue

            # If token is a delimiter char, convert to DELIMITER
            if word in constant.DELIMITERS:
                token.remove_possibility(Tag.CONTEXT_DEPENDENT)
                token.add_possibility(Tag.DELIMITER)
                continue

            # If the keyword entry has regex patterns (designed for glued forms
            # like PART3), but appears separated from a digit (e.g. "part 2"),
            # handle based on context: in brackets → SEQUENCE_PART, in title → demote number.
            entry = token.possibilities[Tag.CONTEXT_DEPENDENT].element
            if entry and entry.regex_dict:
                next_token = cls.get_next_relevant_token(parser, token)
                if next_token and next_token.content.isdigit():
                    if token.bracket_group:
                        token.add_possibility(Tag.SEQUENCE_PART)
                    else:
                        next_token.remove_possibility(Tag.SEQUENCE_NUMBER)

            # Generic fallback: remove CONTEXT_DEPENDENT → title candidate.
            token.remove_possibility(Tag.CONTEXT_DEPENDENT)

    @classmethod
    def handle_plus(cls, parser: AbstractParser, token: Token):
        prev_token = cls.get_previous_relevant_token(parser, token)
        next_token = cls.get_next_relevant_token(parser, token)

        if prev_token and next_token:
            for category, descriptors in prev_token.possibilities.items():
                if not next_token.content.isdigit() and category in [
                    Tag.SEQUENCE_NUMBER,
                ]:
                    continue
                next_token.add_possibility(descriptors.descriptor)

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
