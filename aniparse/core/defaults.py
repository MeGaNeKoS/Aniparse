"""Default configuration: score rules, possibility rules."""
from aniparse.abstraction.parser_base import Possibilities
from aniparse.abstraction.score_base import Score
from aniparse.core.token_tags import Tag


def build_default_score() -> Score:
    from aniparse.rule.scoring.file_checksum_score_rule import FileChecksumScoreRule
    from aniparse.rule.scoring.video_term_score_rule import VideoTermScoreRule
    from aniparse.rule.scoring.audio_term_score_rule import AudioTermScoreRule
    from aniparse.rule.scoring.file_index_score_rule import FileIndexRule
    from aniparse.rule.scoring.sequence_number_score_rule import EpisodeNumberScore
    from aniparse.rule.scoring.video_resolution_score_rule import VideoResolutionScoreRule
    from aniparse.rule.scoring.series_year_score_rule import SeriesYearScore
    from aniparse.rule.scoring.positional_score_rule import PositionalScoreRule
    from aniparse.rule.scoring.contextual_score_rule import ContextualScoreRule

    score = Score()
    score.add_rule(Tag.FILE_CHECKSUM, FileChecksumScoreRule)
    score.add_rule(Tag.VIDEO_TERM, VideoTermScoreRule)
    score.add_rule(Tag.AUDIO_TERM, AudioTermScoreRule)
    score.add_rule(Tag.FILE_INDEX, FileIndexRule)
    score.add_rule(Tag.SEQUENCE_NUMBER, EpisodeNumberScore)
    score.add_rule(Tag.VIDEO_RESOLUTION, VideoResolutionScoreRule)
    score.add_rule(Tag.YEAR, SeriesYearScore)
    score.add_rule(Tag.RELEASE_GROUP, PositionalScoreRule)
    score.add_rule(Tag.LANGUAGE, ContextualScoreRule)
    return score


def build_default_possibilities() -> Possibilities:
    from aniparse.rule.possibilities.number_rule import NumberPossibilityRule
    from aniparse.rule.possibilities.context_dependent_expansion_rule import ContextDependentExpansionPossibilityRule
    from aniparse.rule.possibilities.context_delimiter_rule import ContextDelimiterPossibilityRule
    from aniparse.rule.possibilities.checksum_placeholder_rule import ChecksumPlaceholderPossibilityRule
    from aniparse.rule.possibilities.year_rule import YearPossibilityRule
    from aniparse.rule.possibilities.bracket_content_rule import BracketContentPossibilityRule
    from aniparse.rule.possibilities.release_group_rule import ReleaseGroupPossibilityRule
    from aniparse.rule.possibilities.title_rule import TitlePossibilityRule
    from aniparse.rule.possibilities.zone_assignment_rule import ZoneAssignmentPossibilityRule

    possibilities = Possibilities()
    possibilities.add_rule(ChecksumPlaceholderPossibilityRule)
    possibilities.add_rule(ContextDelimiterPossibilityRule)
    possibilities.add_rule(NumberPossibilityRule)
    possibilities.add_rule(YearPossibilityRule)
    possibilities.add_rule(BracketContentPossibilityRule)
    possibilities.add_rule(ZoneAssignmentPossibilityRule)
    possibilities.add_rule(ContextDependentExpansionPossibilityRule)
    possibilities.add_rule(ReleaseGroupPossibilityRule)
    possibilities.add_rule(TitlePossibilityRule)
    return possibilities
