from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from aniparse.element import DescriptorType
from aniparse.token import Token, Tokens


class ScoreRule(ABC):
    descriptorType = DescriptorType.OTHER

    @classmethod
    @abstractmethod
    def apply(cls, token: Token, tokens: Tokens):
        pass


class Score:
    def __init__(self):
        self.descriptor: dict[DescriptorType, list[Type[ScoreRule]]] = {}

    def add_rule(self, descriptor: DescriptorType, rule: Type[ScoreRule]):
        self.descriptor.setdefault(descriptor, []).append(rule)

    def calculate(self, possibility: DescriptorType, token: Token, tokens: Tokens):
        for rule in self.descriptor.get(possibility, []):
            rule.apply(token, tokens)
