from aniparse.abstraction.score_base import ScoreRule
from aniparse.core.token import Token, Tokens
from aniparse.core.token_tags import Tag

# Labels that represent sequence/episode metadata
SEQUENCE_LABELS = {Tag.SEQUENCE_NUMBER, Tag.SEQUENCE_PREFIX}


class PositionalScoreRule(ScoreRule):
    """Adjust scores based on where a token sits in the filename structure.

    Uses bracket_group info from rhythm analysis to boost/dampen possibilities
    based on positional statistics:
    - First bracket at position 0 strongly correlates with release group
    - Sequence numbers/prefixes are very unlikely in the first bracket
    - Release groups are unlikely in non-first brackets
    """
    descriptorType = Tag.RELEASE_GROUP
    categoryType = Tag.RELEASE_GROUP

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        bg = token.bracket_group
        if bg is None:
            return

        if bg.starts_filename and bg.is_first:
            # First bracket at position 0: statistically release group
            token.add_score(Tag.RELEASE_GROUP, 1.0)
            # Dampen sequence labels — very unlikely here
            for label in SEQUENCE_LABELS:
                if label in token.possibilities:
                    token.add_score(label, -1.0)
            # Dampen year — unlikely in first bracket
            if Tag.YEAR in token.possibilities:
                token.add_score(Tag.YEAR, -0.5)
        else:
            # Non-first brackets: release group is less likely
            if Tag.RELEASE_GROUP in token.possibilities:
                token.add_score(Tag.RELEASE_GROUP, -0.5)
