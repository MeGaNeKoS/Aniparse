import re

from aniparse import constant, ElementCategory

__all__ = ["multi_season_episode_pattern", "multi_season_episode_group"]


def pattern_builder():
    def pattern_optional(*args) -> str:
        return "".join([
            "(?:",
            "".join(args),
            ")?"
        ])

    def pattern_combine(*args):
        last_index = 0
        this_group = {}
        for pattern in args:
            for index in range(1, pattern.groups + 1):
                this_group[index + last_index] = groups[pattern][index]
                if groups[pattern][index] not in this_group:
                    this_group[groups[pattern][index]] = []
                this_group[groups[pattern][index]].append(index + last_index)
            last_index += pattern.groups

        return this_group

    # Make base patterns with the translated group table
    groups = {}
    range_separator = re.compile(rf'([ ~&+{constant.DASHES_PATTERN}])')
    groups[range_separator] = {
        1: ElementCategory.RANGE_SEPARATOR,
        ElementCategory.RANGE_SEPARATOR: [1]
    }

    # <season>x<episode> or <season>[range_separator]e<episode>
    # noinspection RegExpUnnecessaryNonCapturingGroup
    season_episode_separator = re.compile(rf"(?:(x)|([{range_separator.pattern[2:-2]} ._x:])?(e))")
    groups[season_episode_separator] = {
        1: ElementCategory.CONTEXT_DELIMITER,
        2: ElementCategory.RANGE_SEPARATOR,
        3: ElementCategory.CONTEXT_DELIMITER,
        ElementCategory.RANGE_SEPARATOR: [2],
        ElementCategory.CONTEXT_DELIMITER: [1, 3]
    }

    # <number>[.<number>][<release_prefix><release_number>]
    episode_pattern = re.compile(
        r'(\d+(?:\.\d+)?)'  # A number with an optional decimal part (e.g., "01", "01.1")
        r'(?:(v)(\d+))?'  # Optional 'v' followed by a number (e.g., "v2")
    )

    groups[episode_pattern] = {
        1: ElementCategory.EPISODE_NUMBER,
        2: ElementCategory.RELEASE_PREFIX,
        3: ElementCategory.RELEASE_VERSION,
        ElementCategory.EPISODE_NUMBER: [1],
        ElementCategory.RELEASE_PREFIX: [2],
        ElementCategory.RELEASE_VERSION: [3]
    }

    # [prefix]<number>
    season_pattern = re.compile(r"(s)?(\d+)")
    groups[season_pattern] = {
        1: ElementCategory.ANIME_SEASON_PREFIX,
        2: ElementCategory.ANIME_SEASON,
        ElementCategory.ANIME_SEASON_PREFIX: [1],
        ElementCategory.ANIME_SEASON: [2]
    }

    # Expand the patterns and its groups translation
    # <number>[.<number>][<release_prefix><release_number>][<range_separator><number>[.<number>][<release_prefix><release_number>]]
    multi_episode_pattern = re.compile("".join([
        episode_pattern.pattern,
        pattern_optional(
            range_separator.pattern,
            episode_pattern.pattern
        )
    ]))
    groups[multi_episode_pattern] = pattern_combine(episode_pattern, range_separator, episode_pattern)

    # [prefix]<number>[<season_episode_separator><number>[.<number>][<release_prefix><release_number>]]
    season_episode_pattern = re.compile("".join([
        season_pattern.pattern,
        pattern_optional(
            season_episode_separator.pattern,
            episode_pattern.pattern
        )
    ])
    )
    groups[season_episode_pattern] = pattern_combine(season_pattern, season_episode_separator, multi_episode_pattern)

    # [prefix]<number>[<range_separator>[prefix]<number>]
    multi_season_pattern = re.compile("".join([
        season_episode_pattern.pattern,
        pattern_optional(
            range_separator.pattern,
            season_episode_pattern.pattern
        )
    ])
    )
    groups[multi_season_pattern] = pattern_combine(season_episode_pattern, range_separator, season_episode_pattern)

    # [<season>[range_separator]<season>x]<episode>[range_separator]<episode>
    result = re.compile("".join([
        pattern_optional(multi_season_pattern.pattern,
                         season_episode_separator.pattern),
        multi_episode_pattern.pattern,
        "$"
    ])
    )
    return result, pattern_combine(multi_season_pattern,
                                   season_episode_separator,
                                   multi_episode_pattern)


multi_season_episode_pattern, multi_season_episode_group = pattern_builder()


def separate_text(input_string):
    separated_elements = []
    last_end = 0
    for match in re.finditer(multi_season_episode_pattern, input_string):
        start, end = match.span()
        if start > last_end:
            separated_elements.append(input_string[last_end:start])
        for group in match.groups():
            if group is not None:
                separated_elements.append(group)
        last_end = end

    if last_end < len(input_string):
        separated_elements.append(input_string[last_end:])

    return separated_elements
