import re

from aniparse.core import constant
from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser


class ChecksumPlaceholderPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        for entry in parser.word_list_manager.find(constant.CHECKSUM_PLACEHOLDER):
            for regex_expression in entry.regex_dict:
                for match in re.finditer(regex_expression, parser.filename, re.IGNORECASE):
                    matched_tokens = parser.get_matched_tokens_range(match.start(), match.end())
                    if matched_tokens:
                        parser.process_entry(match.group(), matched_tokens, entry)
