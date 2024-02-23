import json

from aniparse import default_word_list_manager
from aniparse.abstraction.ScoreBase import Score
from aniparse.element import Label
from aniparse.parser import Parser
from aniparse.rule.AssingPossibilities.ChecksumPlaceholderRule import ChecksumPlaceholderPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDelimiterRule import ContextDelimiterPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDependentExpansionRule import ContextDependentExpansionPossibilityRule
from aniparse.rule.AssingPossibilities.NumberRule import NumberPossibilityRule
from aniparse.rule.Scoring.AudioTermScoreRule import AudioTermScoreRule
from aniparse.rule.Scoring.FileChecksumScoreRule import FileChecksumScoreRule
from aniparse.rule.Scoring.FileIndexScoreRule import FileIndexRule
from aniparse.rule.Scoring.SequenceNumberScoreRule import EpisodeNumberScore
from aniparse.rule.Scoring.VideoResolutionScoreRule import VideoResolutionScoreRule
from aniparse.rule.Scoring.VideoTermScoreRule import VideoTermScoreRule
from tests.fixtures.table import table

all_table = []
score = Score()
score.add_rule(Label.SEQUENCE_NUMBER, EpisodeNumberScore)
score.add_rule(Label.FILE_INDEX, FileIndexRule)
score.add_rule(Label.VIDEO_RESOLUTION, VideoResolutionScoreRule)
score.add_rule(Label.FILE_CHECKSUM, FileChecksumScoreRule)
score.add_rule(Label.AUDIO_TERM, AudioTermScoreRule)
score.add_rule(Label.VIDEO_TERM, VideoTermScoreRule)

for entry in table:
    filename = entry['file_name']
    if filename == "chrono crusade ep. 1-5":
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
            "possibilities": [(element.value, possibilities) for element, possibilities in token.possibilities.items()]
        })
    print(entry)
    dataset = {
        "filename": filename,
        "input": cleared['tokens'],
        "output": json.dumps(entry)
    }
    all_table.append(dataset)
with open("first_step_parser.json", "w+") as f:
    json.dump(all_table, f, indent=2)
