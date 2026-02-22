from __future__ import annotations

from math import gcd

from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token_tags import Tag
from aniparse.core.token import Token, Tokens
from aniparse.core import constant
from aniparse.core.constant import COMMON_RESOLUTIONS


class VideoResolutionScoreRule(ScoreRule):
    descriptorType = Tag.VIDEO_RESOLUTION

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        if not token.content.isdigit():
            return

        video_resolution_tokens = cls.get_video_resolution_tokens(token, tokens)
        if video_resolution_tokens:
            cls.apply_common_patterns(video_resolution_tokens)
            cls.check_neighbor_tokens(token, tokens, video_resolution_tokens)

    @classmethod
    def check_neighbor_tokens(cls, start_token: Token, tokens: Tokens, video_resolution_tokens: list[Token]):
        # Strong boost for common resolutions inside brackets (e.g. [720], [1080])
        if start_token.content.isdigit() and int(start_token.content) in COMMON_RESOLUTIONS:
            prev_is_bracket = False
            next_is_bracket = False
            for pt in tokens.loop_backward(start_token):
                if Tag.DELIMITER in pt.possibilities:
                    continue
                if Tag.BRACKET in pt.possibilities:
                    prev_is_bracket = True
                break
            for nt in tokens.loop_forward(start_token):
                if Tag.DELIMITER in nt.possibilities:
                    continue
                if Tag.BRACKET in nt.possibilities:
                    next_is_bracket = True
                break
            if prev_is_bracket and next_is_bracket:
                for t in video_resolution_tokens:
                    t.add_score(cls.categoryType, 1.0)

        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                for t in video_resolution_tokens:
                    t.add_score(cls.categoryType, 0.25)
                break
            if Tag.additional_video_information(prev_token.possibilities):
                for t in video_resolution_tokens:
                    t.add_score(cls.categoryType, 0.25)
                for possibility in prev_token.possibilities:
                    if Tag.additional_video_information([possibility]):
                        prev_token.add_score(possibility, 0.25)
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break

        for next_token in tokens.loop_forward(start_token):
            if Tag.BRACKET in next_token.possibilities:
                for t in video_resolution_tokens:
                    t.add_score(cls.categoryType, 0.25)
                break
            if Tag.additional_video_information(next_token.possibilities):
                for t in video_resolution_tokens:
                    t.add_score(cls.categoryType, 0.25)
                for possibility in next_token.possibilities:
                    if Tag.additional_video_information([possibility]):
                        next_token.add_score(possibility, 0.25)
                break
            if Tag.DELIMITER not in next_token.possibilities:
                break

    @classmethod
    def apply_common_patterns(cls, video_resolution_tokens: list[Token]):
        number_tokens = [t for t in video_resolution_tokens if t.content.isdigit()]
        for t in number_tokens:
            if int(t.content) > 100:
                t.add_score(cls.categoryType, 0.25)
            else:
                t.add_score(cls.categoryType, -0.5)
        if len(number_tokens) == 2:
            a = int(number_tokens[0].content)
            b = int(number_tokens[1].content)
            divisor = gcd(a, b)
            simplified_a = a // divisor
            simplified_b = b // divisor
            if simplified_a < simplified_b:
                simplified_a, simplified_b = simplified_b, simplified_a
            aspect_ratios = [
                (4, 3), (16, 9), (185, 100), (235, 100),
                (239, 100), (240, 100), (21, 9),
            ]
            for aspect_ratio in aspect_ratios:
                ratio = simplified_a / simplified_b
                common_ratio_float = aspect_ratio[0] / aspect_ratio[1]
                tolerance = 0.05 * common_ratio_float
                error = abs(ratio - common_ratio_float)
                if error <= tolerance:
                    for t in video_resolution_tokens:
                        t.add_score(Tag.VIDEO_RESOLUTION, round(0.25 * (1 - error), 2))
                    break

        if not number_tokens:
            return

        if len(video_resolution_tokens) == 1:
            if int(number_tokens[0].content) > 100:
                video_resolution_tokens[0].add_score(cls.categoryType, 0.25)
        elif len(video_resolution_tokens) == 2:
            if int(number_tokens[0].content) > 100:
                video_resolution_tokens[0].add_score(cls.categoryType, 0.25)
                if video_resolution_tokens[1].content in constant.VIDEO_RESOLUTION_SUFFIXES:
                    video_resolution_tokens[0].add_score(cls.categoryType, 0.5)
                    video_resolution_tokens[1].add_score(cls.categoryType, 0.5)
            if video_resolution_tokens[1].content in constant.VIDEO_RESOLUTION_MULTIPLIER_SUFFIXES:
                video_resolution_tokens[0].add_score(cls.categoryType, 0.25)
                video_resolution_tokens[1].add_score(cls.categoryType, 0.25)

    @classmethod
    def get_video_resolution_tokens(cls, start_token: Token, tokens: Tokens):
        video_resolution_tokens = []
        for prev_token in tokens.loop_backward(start_token):
            if (Tag.VIDEO_RESOLUTION not in prev_token.possibilities
                    and Tag.DELIMITER not in prev_token.possibilities):
                break
            if Tag.VIDEO_RESOLUTION in prev_token.possibilities:
                video_resolution_tokens.append(prev_token)
        video_resolution_tokens.reverse()
        video_resolution_tokens.append(start_token)
        for next_token in tokens.loop_forward(start_token):
            if Tag.VIDEO_RESOLUTION not in next_token.possibilities:
                break
            video_resolution_tokens.append(next_token)
        return video_resolution_tokens

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        potential_video_resolution_divider = True
        for prev_token in tokens.loop_backward(start_token):
            if Tag.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Tag.BRACKET in next_token.possibilities:
                        start_token.add_score(cls.categoryType, 0.25)
                        break
                    if (potential_video_resolution_divider
                            and len(next_token.content) == 1
                            and not next_token.content.isdigit()):
                        potential_video_resolution_divider = False
                        continue
                    if (Tag.DELIMITER not in next_token.possibilities
                            and not Tag.additional_video_information(next_token.possibilities)):
                        break
                start_token.add_score(cls.categoryType, 0.25)
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break
