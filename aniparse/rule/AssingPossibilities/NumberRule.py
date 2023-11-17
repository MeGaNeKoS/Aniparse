from aniparse import constant
from aniparse.abstraction.ParserBase import PossibilityRule
from aniparse.element import DescriptorType
from aniparse.parser import BaseParser
from aniparse.token import Token


def get_number_from_ordinal(content) -> str:
    return constant.ORDINALS.get(str(content).lower(), "")


class NumberPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: BaseParser):
        for sub_token in parser.tokens:
            if DescriptorType.SEASON_PREFIX in sub_token.possibilities:
                prev_token = cls.get_previous_relevant_token(parser, sub_token)
                if prev_token and get_number_from_ordinal(prev_token.content).isdigit():
                    prev_token.add_possibility(DescriptorType.SEASON_NUMBER)

            if sub_token.content.isdigit() and DescriptorType.FILE_CHECKSUM not in sub_token.possibilities:
                sub_token.add_possibility(DescriptorType.EPISODE_NUMBER)

                # Remove EPISODE_PREFIX if wrongly added before
                if DescriptorType.EPISODE_PREFIX in sub_token.possibilities:
                    sub_token.remove_possibility(DescriptorType.EPISODE_PREFIX)

                prev_token = cls.get_previous_relevant_token(parser, sub_token)
                next_token = cls.get_next_relevant_token(parser, sub_token)

                if not prev_token or not next_token:
                    # File index only can be at the start or the end
                    sub_token.add_possibility(DescriptorType.FILE_INDEX)

                if prev_token and prev_token.content not in constant.BRACKETS:
                    if DescriptorType.SEASON_PREFIX in prev_token.possibilities:
                        sub_token.add_possibility(DescriptorType.SEASON_NUMBER)
                        sub_token.remove_possibility(DescriptorType.EPISODE_NUMBER)
                    if DescriptorType.EPISODE_PREFIX in prev_token.possibilities:
                        sub_token.add_possibility(DescriptorType.EPISODE_NUMBER)

                if next_token and next_token.content not in constant.BRACKETS:
                    for episode_range in parser.tokens.loop_forward(sub_token, next_token):
                        if not episode_range:
                            break

                        if episode_range.content not in constant.RANGE_SEPARATOR:
                            continue
                        if (
                                next_token.content.isdigit() or
                                DescriptorType.EPISODE_NUMBER in next_token.possibilities or
                                DescriptorType.EPISODE_PREFIX in next_token.possibilities or
                                DescriptorType.EPISODE_TOTAL in next_token.possibilities
                        ):
                            if DescriptorType.EPISODE_RANGE not in next_token.possibilities:
                                episode_range.add_possibility(DescriptorType.EPISODE_RANGE)
                    if get_number_from_ordinal(sub_token.content + next_token.content).isdigit():
                        sub_token.add_possibility(DescriptorType.SEASON_NUMBER)
                        sub_token.remove_possibility(DescriptorType.EPISODE_NUMBER)
                        next_token.add_possibility(DescriptorType.SEASON_NUMBER)

                    if DescriptorType.EPISODE_PREFIX in next_token.possibilities:
                        sub_token.add_possibility(DescriptorType.SEASON_NUMBER)
                    if next_token.content.isdigit():
                        # check if there's a token in between
                        if parser.tokens.get_index(next_token) - parser.tokens.get_index(sub_token) > 1:
                            skipped_word = parser.filename[sub_token.index + len(sub_token.content):next_token.index]
                            if len(skipped_word) == 3 and skipped_word[0] == skipped_word[2]:
                                skipped_word = skipped_word[1]
                            if any([char for char in skipped_word.upper() if char in ["."]]):
                                if sub_token.content > next_token.content:
                                    sub_token.add_possibility(DescriptorType.AUDIO_TERM)
                                    next_token.add_possibility(DescriptorType.AUDIO_TERM)
                                elif DescriptorType.AUDIO_TERM in sub_token.possibilities:
                                    next_token.add_possibility(DescriptorType.AUDIO_TERM)

    @staticmethod
    def get_next_relevant_token(parser: BaseParser, current_token: Token):
        for next_token in parser.tokens.loop_forward(current_token):
            if next_token.content in constant.DELIMITERS or next_token.content in constant.BRACKETS:
                continue
            return next_token
        return None

    @staticmethod
    def get_previous_relevant_token(parser, current_token):
        for prev_token in parser.tokens.loop_backward(current_token):
            if prev_token.content in constant.DELIMITERS or prev_token.content in constant.BRACKETS:
                continue
            return prev_token
        return None
