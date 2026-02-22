from aniparse.abstraction.score_base import MetadataScoreRule
from aniparse.core.token_tags import Tag


class VideoTermScoreRule(MetadataScoreRule):
    descriptorType = Tag.VIDEO_TERM
    skip_labels = {Tag.FILE_CHECKSUM}
