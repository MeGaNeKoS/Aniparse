from abc import ABC, abstractmethod
from typing import Type

from aniparse.token_tags import Category, Descriptor
from aniparse.token import Token, Tokens


class ScoreRule(ABC):
    descriptorType: Descriptor = Descriptor.UNKNOWN
    categoryType: Category = Descriptor.to_label(Descriptor.UNKNOWN)

    @classmethod
    @abstractmethod
    def apply(cls, token: Token, tokens: Tokens):
        pass

    def __init_subclass__(cls):
        if cls.descriptorType == Descriptor.UNKNOWN:
            raise ValueError("descriptorType must be set")
        if cls.categoryType == Category.UNKNOWN:
            raise ValueError("categoryType must be set")


class Score:
    def __init__(self):
        self.descriptor: dict[Category, list[Type[ScoreRule]]] = {}

    def add_rule(self, descriptor: Category, rule: Type[ScoreRule]):
        self.descriptor.setdefault(descriptor, []).append(rule)

    def calculate(self, possibility: Category, token: Token, tokens: Tokens):
        for rule in self.descriptor.get(possibility, []):
            rule.apply(token, tokens)
