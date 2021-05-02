import random

from starflake.game_objects.spectrum import Spectrum

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"


class Element:
    """A chemical element."""

    @classmethod
    def random(cls, period):
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

        spectrum = Spectrum.random(period)

        return cls(name, symbol, spectrum)

    def __init__(self, name, symbol, spectrum):
        self.name = name
        self.symbol = symbol
        self.spectrum = spectrum

    def __repr__(self):
        return f"{self.name} ({self.symbol})"
