import random

from starflake.game_objects.constants import COLOURS, CONSONANTS, TABLE_GROUPS, VOWELS


class Element:
    """A chemical element."""

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

    def __init__(self, name, symbol, colours, group_number, period_number):
        self.name = name
        self.symbol = symbol
        self.colours = colours
        self.group_number = group_number
        self.period_number = period_number

    def __repr__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def mass(self):
        """The relative mass of this element."""

        return ((self.period_number - 1) * TABLE_GROUPS) + self.group_number
