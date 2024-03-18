from typing import Union

from aniparse import constant
from aniparse.abstraction.ParserBase import PossibilityRule
from aniparse.token_tags import Category, Descriptor
from aniparse.parser import BaseParser
from aniparse.token import Token


def get_number_from_ordinal(content) -> str:
    return constant.ORDINALS.get(str(content).lower(), "")


class NumberPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: BaseParser):
        for token in parser.tokens:
            if Category.SEQUENCE_PREFIX in token.possibilities:
                # Check for ordinal number like 2nd season
                for prev_token in parser.tokens.loop_backward(token):
                    if prev_token.content in constant.DELIMITERS:
                        continue
                    if get_number_from_ordinal(prev_token.content).isdigit():
                        prev_token.add_possibility(Descriptor.SEQUENCE_NUMBER)
                    break

            # Reduce checking for number that most likely a file checksum
            if token.content.isdigit() and Category.FILE_CHECKSUM not in token.possibilities:
                if int(token.content) > 1990:
                    token.add_possibility(Descriptor.SERIES_YEAR)

                token.add_possibility(Descriptor.SEQUENCE_NUMBER)

                # Remove EPISODE_PREFIX if wrongly added before
                if Category.SEQUENCE_PREFIX in token.possibilities:
                    token.remove_possibility(Category.SEQUENCE_PREFIX)

                prev_token = cls.prev_non_delimiter(parser, token)
                next_token = cls.next_non_delimiter(parser, token)

                if not prev_token or not next_token:
                    # File index only can be at the start or the end
                    token.add_possibility(Descriptor.FILE_INDEX)

                if prev_token and prev_token.content not in constant.BRACKETS:
                    if Category.SEQUENCE_PREFIX in prev_token.possibilities:
                        token.add_possibility(Descriptor.SEQUENCE_NUMBER)

                if next_token and next_token.content not in constant.BRACKETS:
                    for episode_range in parser.tokens.loop_forward(token, next_token):
                        if not episode_range:
                            break

                        if episode_range.content not in constant.RANGE_SEPARATOR:
                            continue
                        if (
                                next_token.content.isdigit() or
                                Category.SEQUENCE_NUMBER in next_token.possibilities or
                                Category.SEQUENCE_PREFIX in next_token.possibilities or
                                Category.SEQUENCE_NUMBER in next_token.possibilities
                        ):
                            if Category.SEQUENCE_RANGE not in next_token.possibilities:
                                episode_range.add_possibility(Descriptor.SEQUENCE_RANGE)
                                next_token.add_possibility(Descriptor.SEQUENCE_NUMBER)

                    if get_number_from_ordinal(token.content + next_token.content).isdigit():
                        token.add_possibility(Descriptor.SEQUENCE_NUMBER)
                        token.remove_possibility(Category.SEQUENCE_NUMBER)
                        next_token.add_possibility(Descriptor.SEQUENCE_NUMBER)

                    if next_token.content.isdigit():
                        # check if there's a token in between
                        if parser.tokens.get_index(next_token) - parser.tokens.get_index(token) > 1:
                            skipped_word = parser.filename[token.index + len(token.content):next_token.index]
                            if len(skipped_word) == 3 and skipped_word[0] == skipped_word[2]:
                                skipped_word = skipped_word[1]
                            if any([char for char in skipped_word.upper() if char in ["."]]):
                                if token.content > next_token.content:
                                    token.add_possibility(Descriptor.AUDIO_TERM)
                                    next_token.add_possibility(Descriptor.AUDIO_TERM)
                                elif Category.AUDIO_TERM in token.possibilities:
                                    next_token.add_possibility(Descriptor.AUDIO_TERM)

    @staticmethod
    def next_non_delimiter(parser: BaseParser, current_token: Token) -> Union[Token, None]:
        for next_token in parser.tokens.loop_forward(current_token):
            if Category.DELIMITER in next_token.possibilities:
                continue
            return next_token
        return None

    @staticmethod
    def prev_non_delimiter(parser, current_token) -> Union[Token, None]:
        for prev_token in parser.tokens.loop_backward(current_token):
            if Category.DELIMITER in prev_token.possibilities:
                continue
            return prev_token
        return None
