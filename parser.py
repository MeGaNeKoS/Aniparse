import enum
import json
from aniparse.parser import Parser
from aniparse.abstraction.ScoreBase import Score
from aniparse import default_word_list_manager
from aniparse.rule.AssingPossibilities.NumberRule import NumberPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDependentExpansionRule import ContextDependentExpansionPossibilityRule
from aniparse.rule.AssingPossibilities.ChecksumPlaceholderRule import ChecksumPlaceholderPossibilityRule
from aniparse.rule.AssingPossibilities.ContextDelimiterRule import ContextDelimiterPossibilityRule
from aniparse.rule.Scoring.SequenceNumberScoreRule import EpisodeNumberScore
from aniparse.element import Label
from aniparse.rule.Scoring.FileIndexScoreRule import FileIndexRule

score = Score()
score.add_rule(Label.SEQUENCE_NUMBER, EpisodeNumberScore)
score.add_rule(Label.FILE_INDEX, FileIndexRule)

class ElementCategory(enum.Enum):
    ANIME_SEASON = 'anime_season'
    ANIME_SEASON_PREFIX = 'anime_season_prefix'
    ANIME_TITLE = 'anime_title'
    ANIME_TITLE_ALT = 'anime_title_alt'
    ANIME_TYPE = 'anime_type'
    ANIME_YEAR = 'anime_year'
    AUDIO_TERM = 'audio_term'
    BATCH = 'batch'
    DEVICE_COMPATIBILITY = 'device_compatibility'
    BRACKET = 'bracket'
    DELIMITER = 'delimiter'
    EPISODE_NUMBER = 'episode_number'
    EPISODE_PART = 'episode_part'
    EPISODE_NUMBER_ALT = 'episode_number_alt'
    EPISODE_PREFIX = 'episode_prefix'
    EPISODE_TITLE = 'episode_title'
    EPISODE_TOTAL = 'episode_total'
    FILE_CHECKSUM = 'file_checksum'
    FILE_EXTENSION = 'file_extension'
    FILE_INDEX = 'file_index'
    FILE_NAME = 'file_name'
    LANGUAGE = 'language'
    OTHER = 'other'
    RANGE_SEPARATOR = 'range_separator'
    RELEASE_GROUP = 'release_group'
    RELEASE_INFORMATION = 'release_information'
    RELEASE_VERSION = 'release_version'
    SOURCE = 'source'
    SUBTITLES = 'subtitles'
    VIDEO_RESOLUTION = 'video_resolution'
    VIDEO_TERM = 'video_term'
    VOLUME_NUMBER = 'volume_number'
    VOLUME_PREFIX = 'volume_prefix'
    UNKNOWN = 'unknown'


category_to_descriptor_mapping = {
    'ANIME_SEASON': 'SEASON_NUMBER',
    'ANIME_SEASON_PREFIX': 'SEASON_PREFIX',
    'ANIME_TITLE': 'SERIES_TITLE',
    'ANIME_TITLE_ALT': 'SERIES_TITLE',  # Assuming alternate titles can be treated the same
    'ANIME_TYPE': 'SERIES_TYPE',
    'ANIME_YEAR': 'SERIES_YEAR',
    'AUDIO_TERM': 'AUDIO_TERM',
    'BATCH': 'OTHER',  # If 'BATCH' has no direct equivalent, mapping to 'OTHER'
    'DEVICE_COMPATIBILITY': 'DEVICE_COMPATIBILITY',
    'BRACKET': 'BRACKET',
    'DELIMITER': 'DELIMITER',
    'EPISODE_NUMBER': 'EPISODE_NUMBER',
    'EPISODE_PART': 'OTHER',  # No direct equivalent, assuming a generic categorization
    'EPISODE_NUMBER_ALT': 'EPISODE_NUMBER',  # Assuming alternate numbers can be treated the same
    'EPISODE_PREFIX': 'EPISODE_PREFIX',
    'EPISODE_TITLE': 'EPISODE_TITLE',
    'EPISODE_TOTAL': 'EPISODE_TOTAL',
    'FILE_CHECKSUM': 'FILE_CHECKSUM',
    'FILE_EXTENSION': 'FILE_EXTENSION',
    'FILE_INDEX': 'FILE_INDEX',
    'FILE_NAME': 'FILE_NAME',
    'LANGUAGE': 'LANGUAGE',
    'OTHER': 'OTHER',
    'RANGE_SEPARATOR': 'EPISODE_RANGE',
    'RELEASE_GROUP': 'RELEASE_GROUP',
    'RELEASE_INFORMATION': 'RELEASE_INFORMATION',
    'RELEASE_VERSION': 'RELEASE_VERSION',
    'SOURCE': 'SOURCE',
    'SUBTITLES': 'SUBS_TERM',
    'VIDEO_RESOLUTION': 'VIDEO_RESOLUTION',
    'VIDEO_TERM': 'VIDEO_TERM',
    'VOLUME_NUMBER': 'VOLUME_NUMBER',
    'VOLUME_PREFIX': 'VOLUME_PREFIX',
    'UNKNOWN': 'UNKNOWN'
}

def remap_keys(entry, mapping):
    remapped_entry = {}
    for key, value in entry.items():
        new_key = mapping.get(key, key)  # Use the new key if it exists in the mapping, else keep the old key
        remapped_entry[new_key] = value
    return remapped_entry

with open('output_1.jsonl', 'r') as file, open('output_2.jsonl', 'w') as output_file:
    for line in file:
        entry = json.loads(line)
        filename = entry['file_name']
        parser = Parser(filename, default_word_list_manager, possibility_rule=[
            ChecksumPlaceholderPossibilityRule,
            NumberPossibilityRule,
            ContextDependentExpansionPossibilityRule,
            ContextDelimiterPossibilityRule
        ], score=score)
        parser.parse()

        cleared = {"file_name": filename, "tokens": []}
        for token in parser.tokens:
            cleared['tokens'].append({
                "content": token.content,
                # "index": token.index,
                "possibilities": [element.value for element, possibilities in token.possibilities.items()]
            })

        remapped_entry = remap_keys(entry, category_to_descriptor_mapping)
        remapped_entry.pop('file_name', None)
        dataset = {
            "filename": filename,
            "input": json.dumps(cleared['tokens']),
            "output": json.dumps(remapped_entry)
        }

        output_file.write(json.dumps(dataset) + '\n')