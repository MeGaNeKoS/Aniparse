from aniparse.abstraction.score_base import MetadataScoreRule
from aniparse.core.token_tags import Tag


class AudioTermScoreRule(MetadataScoreRule):
    descriptorType = Tag.AUDIO_TERM
    skip_labels = {Tag.FILE_CHECKSUM}
