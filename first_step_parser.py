import json

from aniparse import default_word_list_manager
from aniparse.abstraction.ScoreBase import Score
from aniparse.token_tags import Category
from aniparse.output_schemas import Metadata
from aniparse.parser import Parser
from aniparse.rule.Possibilities.ChecksumPlaceholderRule import ChecksumPlaceholderPossibilityRule
from aniparse.rule.Possibilities.ContextDelimiterRule import ContextDelimiterPossibilityRule
from aniparse.rule.Possibilities.ContextDependentExpansionRule import ContextDependentExpansionPossibilityRule
from aniparse.rule.Possibilities.NumberRule import NumberPossibilityRule
from aniparse.rule.Scoring.AudioTermScoreRule import AudioTermScoreRule
from aniparse.rule.Scoring.FileChecksumScoreRule import FileChecksumScoreRule
from aniparse.rule.Scoring.FileIndexScoreRule import FileIndexRule
from aniparse.rule.Scoring.SequenceNumberScoreRule import EpisodeNumberScore
from aniparse.rule.Scoring.SeriesYear import SeriesYearScore
from aniparse.rule.Scoring.VideoResolutionScoreRule import VideoResolutionScoreRule
from aniparse.rule.Scoring.VideoTermScoreRule import VideoTermScoreRule
from tests.fixtures.table import table

all_table = []
score = Score()
score.add_rule(Category.SEQUENCE_NUMBER, EpisodeNumberScore)
score.add_rule(Category.FILE_INDEX, FileIndexRule)
score.add_rule(Category.VIDEO_RESOLUTION, VideoResolutionScoreRule)
score.add_rule(Category.FILE_CHECKSUM, FileChecksumScoreRule)
score.add_rule(Category.AUDIO_TERM, AudioTermScoreRule)
score.add_rule(Category.VIDEO_TERM, VideoTermScoreRule)
score.add_rule(Category.YEAR, SeriesYearScore)

for entry in table:  # type:Metadata
    filename = entry.file_name
    if filename == "[judas] granblue fantasy - clean ending":
        print(f"checking {filename}")
    parser = Parser(filename, default_word_list_manager, possibility_rule=[
        ChecksumPlaceholderPossibilityRule,
        NumberPossibilityRule,
        ContextDependentExpansionPossibilityRule,
        ContextDelimiterPossibilityRule
    ], score=score)
    parser.parse()

    cleared = {"file_name": filename}
    cleared['tokens'] = []
    for token in parser.tokens:
        cleared['tokens'].append({
            "content": token.content,
            # "index": token.index,
            "possibilities": [(element.value, possibilities["score"]) for element, possibilities in token.possibilities.items()]
        })
    print(entry)
    dataset = {
        "filename": filename,
        "input": cleared['tokens'],
        "output": entry.to_dict()
    }
    all_table.append(dataset)
with open("first_step_parser.json", "w+") as f:
    json.dump(all_table, f, indent=2)
