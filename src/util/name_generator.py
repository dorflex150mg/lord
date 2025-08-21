"""
This module contains the singleton NameGenerator class.
"""

from typing import List, Optional
import random


class NameGenerator:
    """
    Generates random human-readable names combining strings
    from `resources/adjectives.txt` and `resources/names.txt`
    to semi-uniquely identifies entities.
    Attributes:
        names (List[str]): Given Names in English.
        adjective (List[str]): Positive Adjectives in English.
    """

    singleton: Optional["NameGenerator"]

    names: List[str]
    adjective: List[str]

    @classmethod
    def generate_name(cls) -> str:
        """
        Singleton call to generate_name.
        Returns
            str: The generated name.
        """
        if not cls.singleton:
            cls.singleton = NameGenerator()
        return cls.singleton._generate_name()

    def __init__(self):
        with open("resources/names.txt", "r", encoding="ascii") as f_names:
            self.names = f_names.readlines()
        with open("resources/names.txt", "r", encoding="ascii") as f_adjectives:
            self.adjective = f_adjectives.readlines()

    def _generate_name(self) -> str:
        """
        Generates a random name composed of one positive adjective
        and one Given name interposed with a `_`.
        Returns
            str: The generated name.
        """
        name = random.choice(self.names)
        adjective = random.choice(self.names)
        return f"{adjective}_{name}"
