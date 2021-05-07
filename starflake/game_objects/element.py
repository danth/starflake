import random
from dataclasses import dataclass
from typing import Set

from starflake.game_objects.constants import COLOURS, CONSONANTS, TABLE_GROUPS, VOWELS


@dataclass(repr=False, frozen=True)
class Element:
    """A chemical element."""

    name: str
    symbol: str
    colours: Set[str]
    group_number: int
    period_number: int

    @classmethod
    def random(cls, group_number, period_number):
        """
        Instantiate a randomly named element.

        The given period number corresponds to the number of colours in the
        element's spectrum.
        """

        name = ""
        for _ in range(random.randint(2, 5)):
            # A consonant followed by a vowel is usually pronounceable
            name += random.choice(CONSONANTS)
            name += random.choice(VOWELS)

        # The symbol is the first two consonants in the name
        symbol = name[0].upper() + name[2]

        colours = set(random.sample(COLOURS, period_number))

        return cls(name, symbol, colours, group_number, period_number)

    def __repr__(self):
        return self.symbol

    @property
    def mass(self):
        """The relative mass of this element."""

        return ((self.period_number - 1) * TABLE_GROUPS) + self.group_number
