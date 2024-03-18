from math import gcd

from aniparse.abstraction.ScoreBase import ScoreRule
from aniparse.token_tags import Category
from aniparse.token import Token, Tokens


class VideoResolutionScoreRule(ScoreRule):
    descriptorType = Category.VIDEO_RESOLUTION

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
        for prev_token in tokens.loop_backward(start_token):
            if Category.BRACKET in prev_token.possibilities:
                for token in video_resolution_tokens:
                    token.possibilities[cls.descriptorType]["score"] += 0.25
                break
            if Category.additional_video_information(prev_token.possibilities):
                for token in video_resolution_tokens:
                    token.possibilities[cls.descriptorType]["score"] += 0.25
                for possibilities in prev_token.possibilities:
                    if Category.additional_video_information([possibilities]):
                        prev_token.possibilities[possibilities]["score"] += 0.25
                break
            if Category.DELIMITER not in prev_token.possibilities:
                break

        for next_token in tokens.loop_forward(start_token):
            if Category.BRACKET in next_token.possibilities:
                for token in video_resolution_tokens:
                    token.possibilities[cls.descriptorType]["score"] += 0.25
                break

            if Category.additional_video_information(next_token.possibilities):
                for token in video_resolution_tokens:
                    token.possibilities[cls.descriptorType]["score"] += 0.25

                for possibilities in next_token.possibilities:
                    if Category.additional_video_information([possibilities]):
                        next_token.possibilities[possibilities]["score"] += 0.25
                break
            if Category.DELIMITER not in next_token.possibilities:
                break

    @classmethod
    def apply_common_patterns(cls, video_resolution_tokens: list[Token]):
        # Get all number tokens
        number_tokens = [token for token in video_resolution_tokens if token.content.isdigit()]
        # Usually video resolution over 480p
        for token in number_tokens:
            if int(token.content) > 100:
                token.possibilities[cls.descriptorType]["score"] += 0.25
            else:
                token.possibilities[cls.descriptorType]["score"] -= 0.5
        if len(number_tokens) == 2:
            # Calculate the video resolution ratio like 16:9, 4:3, etc
            a = int(number_tokens[0].content)
            b = int(number_tokens[1].content)
            divisor = gcd(a, b)
            simplified_a = a // divisor
            simplified_b = b // divisor
            # We treat as a horizontal aspect ratio
            if simplified_a < simplified_b:
                simplified_a, simplified_b = simplified_b, simplified_a
            # Common video aspect ratios list
            aspect_ratios = [
                (4, 3),  # Traditional TV and early DVDs, NTSC standard
                (16, 9),  # Standard for HDTV, modern DVDs, Blu-ray, and online video
                (185, 100),  # Common in American and British cinema (approximated from 1.85:1)
                (235, 100),  # CinemaScope, widescreen cinematic films (approximated from 2.35:1)
                (239, 100),  # Similar to 2.35:1, used for many cinematic films (approximated from 2.39:1)
                (240, 100),  # Essentially the same as 2.39:1, common cinematic widescreen (approximated from 2.40:1)
                (21, 9),  # UltraWide, for computer monitors and home cinema
            ]
            for aspect_ratio in aspect_ratios:
                ratio = simplified_a / simplified_b
                # Calculate the float ratio of the common aspect ratio
                common_ratio_float = aspect_ratio[0] / aspect_ratio[1]
                # Define a tolerance level, e.g., 5% of the common_ratio
                tolerance = 0.05 * common_ratio_float
                # Check if the calculated ratio is within the tolerance of the common ratio
                error = abs(ratio - common_ratio_float)
                if error <= tolerance:
                    for token in video_resolution_tokens:
                        # 0.25 because we're going to apply this twice, [1920 (1), x, 1080 (2)]
                        token.possibilities[Category.VIDEO_RESOLUTION]["score"] += round(0.25 * (1 - error), 2)
                    break

        # Check for other common format like [xxx], [xxx, p], [xxx, i], [x, k]
        if len(video_resolution_tokens) == 1:
            if int(number_tokens[0].content) > 100:
                video_resolution_tokens[0].possibilities[cls.descriptorType]["score"] += 0.25
        elif len(video_resolution_tokens) == 2:
            if int(number_tokens[0].content) > 100:
                video_resolution_tokens[0].possibilities[cls.descriptorType]["score"] += 0.25
                if video_resolution_tokens[1].content in ['p', 'i']:
                    video_resolution_tokens[0].possibilities[cls.descriptorType]["score"] += 0.5
                    video_resolution_tokens[1].possibilities[cls.descriptorType]["score"] += 0.5
            if video_resolution_tokens[1].content in ['k']:
                video_resolution_tokens[0].possibilities[cls.descriptorType]["score"] += 0.25
                video_resolution_tokens[1].possibilities[cls.descriptorType]["score"] += 0.25

    @classmethod
    def get_video_resolution_tokens(cls, start_token: Token, tokens: Tokens):
        video_resolution_tokens = []
        for prev_token in tokens.loop_backward(start_token):
            if (Category.VIDEO_RESOLUTION not in prev_token.possibilities
                    and Category.DELIMITER not in prev_token.possibilities):
                break
            if Category.VIDEO_RESOLUTION in prev_token.possibilities:
                video_resolution_tokens.append(prev_token)
        video_resolution_tokens.reverse()
        video_resolution_tokens.append(start_token)
        for next_token in tokens.loop_forward(start_token):
            if Category.VIDEO_RESOLUTION not in next_token.possibilities:
                break
            video_resolution_tokens.append(next_token)
        return video_resolution_tokens

    @classmethod
    def apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        potential_video_resolution_divider = True
        for prev_token in tokens.loop_backward(start_token):
            if Category.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if Category.BRACKET in next_token.possibilities:
                        start_token.possibilities[cls.descriptorType]["score"] += 0.25
                        break
                    # This could be video resolution divider (x) or information (p, i)
                    if (potential_video_resolution_divider
                            and len(next_token.content) == 1
                            and not next_token.content.isdigit()):
                        potential_video_resolution_divider = False
                        continue

                    if (Category.DELIMITER not in next_token.possibilities
                            and not Category.additional_video_information(next_token.possibilities)):
                        break

                start_token.possibilities[cls.descriptorType]["score"] += 0.25
                break
            if Category.DELIMITER not in prev_token.possibilities:
                break
