import json
from aniparse.parser import Parser
from aniparse.abstraction.ScoreBase import Score
from tests.fixtures.table import table
from aniparse import default_word_list_manager
from aniparse.rule.AssingPossibilities.NumberRule import NumberPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDependentExpansionRule import ContextDependentExpansionPossibilityRule
from aniparse.rule.AssingPossibilities.ChecksumPlaceholderRule import ChecksumPlaceholderPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDelimiterRule import ContextDelimiterPossibilityRule
from aniparse.rule.Scoring.EpisodeNumberScoreRule import EpisodeNumberScoreP
from aniparse.element import DescriptorType
all_table = []
score = Score()
score.add_rule(DescriptorType.EPISODE_NUMBER, EpisodeNumberScoreP)
for entry in table:
    filename = entry['file_name']
    if filename == "evangelion shin gekijouban q (bdrip 1920x1080 x264 flacx2 5.1.8)-ank":
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
            "index": token.index,
            "possibilities": {element.value: possibilities for element, possibilities in token.possibilities.items()}
        })
    all_table.append(cleared)
with open("first_step_parser.json", "w+") as f:
    json.dump(all_table, f, indent=2)
