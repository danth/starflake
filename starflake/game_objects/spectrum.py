import random
from dataclasses import dataclass
from typing import Set

from starflake.game_objects import RandomisableGameObject, BondableGameObject
from starflake.game_objects.constants import COLOURS


@dataclass(frozen=True)
class Spectrum(RandomisableGameObject, BondableGameObject):
    """A set of colours, used to determine molecular bonding."""

    colours: Set[str]

    @classmethod
    def random(cls, colour_count):
        colours = random.sample(COLOURS, colour_count)
        return cls(set(colours))

    @property
    def emoji(self):
        """A representation of this spectrum as Discord emojis."""

        spectrum = ""

        for colour in COLOURS:
            if colour in self.colours:
                spectrum += f":{colour}_circle:"
            else:
                spectrum += ":black_circle:"

        return spectrum

    def can_bond(self, other):
        # Ensure the set intersection is empty
        return len(self.colours & other.colours) == 0

    def bond(self, other):
        colours = self.colours.union(other.colours)
        return Spectrum(colours)
