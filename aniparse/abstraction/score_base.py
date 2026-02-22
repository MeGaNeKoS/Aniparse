from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from aniparse.core.token import Token, Tokens
from aniparse.core.token_tags import Tag


class ScoreRule(ABC):
    descriptorType: Tag = Tag.UNKNOWN
    categoryType: Tag

    @classmethod
    @abstractmethod
    def apply(cls, token: Token, tokens: Tokens):
        pass

    def __init_subclass__(cls):
        if cls.descriptorType == Tag.UNKNOWN:
            return
        cls.categoryType = cls.descriptorType.group


class Score:
    def __init__(self):
        self.descriptor: dict[Tag, list[Type[ScoreRule]]] = {}

    def add_rule(self, descriptor: Tag, rule: Type[ScoreRule]):
        self.descriptor.setdefault(descriptor, []).append(rule)

    def calculate(self, possibility: Tag, token: Token, tokens: Tokens):
        for rule in self.descriptor.get(possibility, []):
            rule.apply(token, tokens)


class MetadataScoreRule(ScoreRule):
    """Base for metadata score rules (AudioTerm, VideoTerm, FileChecksum).

    Provides shared bracket-proximity and neighbor-boosting logic.
    Subclasses set descriptorType and skip_labels.
    """
    skip_labels: set[Tag] = set()

    @classmethod
    def apply(cls, token: Token, tokens: Tokens):
        cls._apply_in_bracket_rules(token, tokens)
        cls._check_neighbor_token(token, tokens)

    @classmethod
    def _should_skip(cls, token: Token) -> bool:
        for label in cls.skip_labels:
            if label in token.possibilities:
                return True
        return False

    @classmethod
    def _apply_in_bracket_rules(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if cls._should_skip(prev_token):
                continue
            if Tag.BRACKET in prev_token.possibilities:
                for next_token in tokens.loop_forward(start_token):
                    if cls._should_skip(next_token):
                        continue
                    if Tag.BRACKET in next_token.possibilities:
                        start_token.add_score(cls.categoryType, 0.25)
                        break
                    if Tag.DELIMITER not in next_token.possibilities:
                        break
                start_token.add_score(cls.categoryType, 0.25)
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break

    @classmethod
    def _check_neighbor_token(cls, start_token: Token, tokens: Tokens):
        for prev_token in tokens.loop_backward(start_token):
            if cls._should_skip(prev_token):
                continue
            flag = False
            for possibility in prev_token.possibilities:
                if possibility in Tag.get_optional_info():
                    if possibility == cls.categoryType:
                        continue
                    prev_token.add_score(possibility, 0.25)
                    flag = True
            if flag:
                start_token.add_score(cls.categoryType, 0.25)
                break
            if Tag.DELIMITER not in prev_token.possibilities:
                break

        for next_token in tokens.loop_forward(start_token):
            if cls._should_skip(next_token):
                continue
            flag = False
            for possibility in next_token.possibilities:
                if possibility in Tag.get_optional_info():
                    if possibility == cls.categoryType:
                        continue
                    next_token.add_score(possibility, 0.25)
                    flag = True
            if flag:
                start_token.add_score(cls.categoryType, 0.25)
                break
            if Tag.DELIMITER not in next_token.possibilities:
                break
