from aniparse.core import constant
from aniparse.abstraction.score_base import MetadataScoreRule
from aniparse.core.token_tags import Tag
from aniparse.core.token import Token, Tokens


class FileChecksumScoreRule(MetadataScoreRule):
    descriptorType = Tag.FILE_CHECKSUM
    skip_labels = set()

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        super().apply(token, tokens)
        cls._boost_checksum_neighbors(token, tokens)

    VALID_CHECKSUM_LENGTHS = {8}  # CRC32

    @classmethod
    def _boost_checksum_neighbors(cls, token: Token, tokens: Tokens):
        """Boost score when adjacent tokens also have FILE_CHECKSUM and concatenated length is valid."""
        # Collect the full contiguous FILE_CHECKSUM span by walking both directions
        span = [token]
        for neighbor in tokens.loop_backward(token):
            if Tag.DELIMITER in neighbor.possibilities:
                continue
            if Tag.FILE_CHECKSUM in neighbor.possibilities:
                span.insert(0, neighbor)
                continue
            break
        for neighbor in tokens.loop_forward(token):
            if Tag.DELIMITER in neighbor.possibilities:
                continue
            if Tag.FILE_CHECKSUM in neighbor.possibilities:
                span.append(neighbor)
                continue
            break

        if len(span) > 1:
            concat_len = sum(len(t.content) for t in span)
            if concat_len in cls.VALID_CHECKSUM_LENGTHS:
                # Strong boost — checksum with valid CRC32 length
                token.add_score(cls.categoryType, 2.0)
            else:
                token.add_score(cls.categoryType, -0.5)
