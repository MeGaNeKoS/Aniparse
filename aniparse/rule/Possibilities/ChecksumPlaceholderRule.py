import re

from aniparse import constant
from aniparse.abstraction.ParserBase import PossibilityRule
from aniparse.parser import BaseParser


class ChecksumPlaceholderPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: BaseParser):
        for entry in parser.word_list_manager.exists(constant.CHECKSUM_PLACEHOLDER):
            for regex_expression in entry.regex_dict:
                for match in re.finditer(regex_expression, parser.filename, re.IGNORECASE):
                    start_pos = match.start()
                    token = parser.tokens.get_token(start_pos)
                    if token:
                        parser.process_entry(token.content, [token], entry)
