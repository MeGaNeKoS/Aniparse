from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from aniparse.element import Label
from aniparse.token import Token, Tokens


class ScoreRule(ABC):
    descriptorType = Label.UNKNOWN

    @classmethod
    @abstractmethod
    def apply(cls, token: Token, tokens: Tokens):
        pass


class Score:
    def __init__(self):
        self.descriptor: dict[Label, list[Type[ScoreRule]]] = {}

    def add_rule(self, descriptor: Label, rule: Type[ScoreRule]):
        self.descriptor.setdefault(descriptor, []).append(rule)

    def calculate(self, possibility: Label, token: Token, tokens: Tokens):
        for rule in self.descriptor.get(possibility, []):
            rule.apply(token, tokens)
