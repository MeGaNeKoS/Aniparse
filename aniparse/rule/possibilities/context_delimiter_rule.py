from aniparse.abstraction.parser_base import PossibilityRule, AbstractParser
from aniparse.core.token_tags import Tag


class ContextDelimiterPossibilityRule(PossibilityRule):
    @classmethod
    def apply(cls, parser: AbstractParser):
        profile = parser.delimiter_profile

        if profile.file_index_end is not None:
            first_token = parser.tokens.tokens[0] if parser.tokens.tokens else None
            if first_token and first_token.content.isdigit():
                first_token.add_possibility(Tag.FILE_INDEX)

        for token in parser.tokens:
            if Tag.CONTEXT_DELIMITER not in token.possibilities and Tag.DELIMITER not in token.possibilities:
                continue

            if Tag.DELIMITER in token.possibilities:
                # Skip ABA promotion when delimiter is uniform and matches primary
                if profile.is_uniform and token.content == profile.primary:
                    continue

                prev_token = parser.tokens.find_prev(token)
                next_token = parser.tokens.find_next(token)

                if prev_token and next_token:
                    if (Tag.DELIMITER in prev_token.possibilities and
                            Tag.DELIMITER in next_token.possibilities and
                            prev_token.content == next_token.content != token.content):
                        token.remove_possibility(Tag.DELIMITER)
                        token.add_possibility(Tag.CONTEXT_DELIMITER)
