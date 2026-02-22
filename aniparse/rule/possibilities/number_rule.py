from typing import Union

from aniparse.config import ParserConfig
from aniparse.core import constant
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag
from aniparse.core.token import Token


def get_number_from_ordinal(content, config: ParserConfig) -> str:
    lower = str(content).lower()
    # Word ordinals (first, second, ...)
    val = config.ordinals.get(lower)
    if val:
        return val
    # Numeric ordinals (1st, 22nd, ...) — strip suffix
    for suffix in config.ordinal_suffixes:
        if lower.endswith(suffix):
            num_part = lower[:-len(suffix)]
            if num_part.isdigit():
                return num_part
    return ""


class NumberPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        config = parser.config
        for token in parser.tokens:
            if Tag.SEQUENCE_PREFIX in token.possibilities:
                # Check for ordinal number like 2nd season
                for prev_token in parser.tokens.loop_backward(token):
                    if prev_token.content in constant.DELIMITERS:
                        continue
                    if get_number_from_ordinal(prev_token.content, config).isdigit():
                        prev_token.add_possibility(Tag.SEQUENCE_NUMBER)
                    break

                # SEQUENCE_NUMBER + EPISODE_PREFIX + SEQUENCE_NUMBER →
                # the preceding number is a season number
                poss = token.possibilities[Tag.SEQUENCE_PREFIX]
                if poss.descriptor == Tag.EPISODE:
                    prev = cls.prev_non_delimiter(parser, token)
                    nxt = cls.next_non_delimiter(parser, token)
                    if (prev and Tag.SEQUENCE_NUMBER in prev.possibilities
                            and nxt and Tag.SEQUENCE_NUMBER in nxt.possibilities):
                        prev.possibilities[Tag.SEQUENCE_NUMBER].descriptor = Tag.SEASON

            # Reduce checking for number that most likely a file checksum
            if token.content.isdigit() and Tag.FILE_CHECKSUM not in token.possibilities:
                num_val_year = int(token.content)
                if config.year_min <= num_val_year <= config.year_max:
                    token.add_possibility(Tag.SERIES_YEAR)

                token.add_possibility(Tag.SEQUENCE_NUMBER)

                # Check for episode part suffix (e.g. "111c" → "c" is part)
                next_tok = cls.next_non_delimiter(parser, token)
                if (next_tok and len(next_tok.content) == 1
                        and next_tok.content.isalpha()
                        and next_tok.index == token.index + len(token.content)
                        and Tag.SEQUENCE_PREFIX not in next_tok.possibilities):
                    next_tok.add_possibility(Tag.SEQUENCE_PART, base_score=1.5)

                # Common bare resolution values (e.g. "1080" without "p")
                num_val = int(token.content)
                if num_val in constant.COMMON_RESOLUTIONS:
                    token.add_possibility(Tag.VIDEO_RESOLUTION)

                # Remove EPISODE_PREFIX if wrongly added before
                if Tag.SEQUENCE_PREFIX in token.possibilities:
                    token.remove_possibility(Tag.SEQUENCE_PREFIX)

                prev_token = cls.prev_non_delimiter(parser, token)
                next_token = cls.next_non_delimiter(parser, token)

                if not prev_token or not next_token:
                    # File index only can be at the start or the end
                    token.add_possibility(Tag.FILE_INDEX)

                if prev_token and prev_token.content not in constant.BRACKETS:
                    if Tag.SEQUENCE_PREFIX in prev_token.possibilities:
                        token.add_possibility(Tag.SEQUENCE_NUMBER)

                if next_token and next_token.content not in constant.BRACKETS:
                    for episode_range in parser.tokens.loop_forward(token, next_token):
                        if not episode_range:
                            break

                        if episode_range.content not in config.range_separator:
                            continue
                        if (
                                next_token.content.isdigit() or
                                Tag.SEQUENCE_NUMBER in next_token.possibilities or
                                Tag.SEQUENCE_PREFIX in next_token.possibilities or
                                Tag.SEQUENCE_NUMBER in next_token.possibilities
                        ):
                            if Tag.SEQUENCE_RANGE not in next_token.possibilities:
                                episode_range.add_possibility(Tag.SEQUENCE_RANGE)
                                next_token.add_possibility(Tag.SEQUENCE_NUMBER)

                    if get_number_from_ordinal(token.content + next_token.content, config).isdigit():
                        token.add_possibility(Tag.SEQUENCE_NUMBER)
                        token.remove_possibility(Tag.SEQUENCE_NUMBER)
                        next_token.add_possibility(Tag.SEQUENCE_NUMBER)

                    if next_token.content.isdigit():
                        # check if there's a token in between
                        if parser.tokens.get_index(next_token) - parser.tokens.get_index(token) > 1:
                            skipped_word = parser.filename[token.index + len(token.content):next_token.index]
                            if len(skipped_word) == 3 and skipped_word[0] == skipped_word[2]:
                                skipped_word = skipped_word[1]
                            if constant.DOT in skipped_word:
                                if (token.content > next_token.content and int(token.content) >= 2
                                        and Tag.VIDEO_TERM not in token.possibilities):
                                    token.add_possibility(Tag.AUDIO_TERM, base_score=1.5)
                                    next_token.add_possibility(Tag.AUDIO_TERM, base_score=1.5)
                                    # Tag the dot between them as AUDIO_TERM too
                                    for mid in parser.tokens.loop_forward(token):
                                        if mid is next_token:
                                            break
                                        if Tag.DELIMITER in mid.possibilities and mid.content == constant.DOT:
                                            mid.add_possibility(Tag.AUDIO_TERM, base_score=0.5)
                                elif Tag.AUDIO_TERM in token.possibilities:
                                    next_token.add_possibility(Tag.AUDIO_TERM)
                                    for mid in parser.tokens.loop_forward(token):
                                        if mid is next_token:
                                            break
                                        if Tag.DELIMITER in mid.possibilities and mid.content == constant.DOT:
                                            mid.add_possibility(Tag.AUDIO_TERM, base_score=0.5)

    @staticmethod
    def next_non_delimiter(parser: AbstractParser, current_token: Token) -> Union[Token, None]:
        for next_token in parser.tokens.loop_forward(current_token):
            if Tag.DELIMITER in next_token.possibilities:
                continue
            return next_token
        return None

    @staticmethod
    def prev_non_delimiter(parser, current_token) -> Union[Token, None]:
        for prev_token in parser.tokens.loop_backward(current_token):
            if Tag.DELIMITER in prev_token.possibilities:
                continue
            return prev_token
        return None
