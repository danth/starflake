import random

from starflake.game_objects.colour import Colour


class Spectrum:
    """A collection of colour spots, used to determine the bonding of elements."""

    @classmethod
    def random(cls, colour_count):
        """Instantiate a random spectrum."""

        colours = []

        def is_acceptable(new_colour):
            """Ensure a colour does not overlap another colour in the list."""
            return not any(
                colour.overlaps(new_colour)
                for colour in colours
            )

        while len(colours) < colour_count:
            colour = Colour.random()
            if is_acceptable(colour):
                colours.append(colour)

        return cls(colours)

    def __init__(self, colours):
        self.colours = colours

    def __repr__(self):
        return f"Spectrum({self.colours})"

    @property
    def mean_hue(self):
        """The average hue of the colours in this spectrum."""

        return sum(colour.hue for colour in self.colours) / len(self.colours)

    def bonds(self, other):
        """Return the number of bonds formed when combining with another spectrum."""

        bonds = 0

        for colour in self.colours:
            for other_colour in other.colours:
                if colour.overlaps(other_colour):
                    bonds += 1

        return bonds
