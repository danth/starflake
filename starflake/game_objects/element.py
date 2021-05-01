import random

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"


class Element:
    """A chemical element."""

    @classmethod
    def random(cls):
        """Instantiate a randomly named element."""

        name = ""
        for _ in range(random.randint(2, 5)):
            # A consonant followed by a vowel is usually pronounceable
            name += random.choice(CONSONANTS)
            name += random.choice(VOWELS)

        # The symbol is the first two consonants in the name
        symbol = name[0].upper() + name[2]

        return cls(name, symbol)

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return f"{self.name} ({self.symbol})"
