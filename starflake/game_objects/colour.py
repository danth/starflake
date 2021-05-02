import random

MINIMUM_COLOUR_WIDTH = 0.005
MAXIMUM_COLOUR_WIDTH = 0.05

# Used alongside the hue when displaying colours in Discord
SATURATION = 0.7
VALUE = 0.7


class Colour:
    """A spot of colour which covers a small range of hues."""

    @classmethod
    def random(cls):
        """Instantiate a random colour spot."""

        hue = random.random()
        width = random.uniform(MINIMUM_COLOUR_WIDTH, MAXIMUM_COLOUR_WIDTH)

        return cls(hue, width)

    def __init__(self, hue, width):
        self.hue = hue
        self.width = width

    def __repr__(self):
        return f"Colour({self.hue:.3f}, {self.width:.3f})"

    @property
    def lower_bound(self):
        """The lowest hue covered by this colour spot."""

        return (self.hue - (self.width / 2)) % 1

    @property
    def upper_bound(self):
        """The highest hue covered by this colour spot."""

        return (self.hue + (self.width / 2)) % 1

    def overlaps(self, other):
        """Return whether this colour overlaps the given colour."""

        # https://stackoverflow.com/a/325964
        return not (
            # This colour's range is entirely below the other colour's range
            self.upper_bound < other.lower_bound
            # This colour's range is entirely above the other colour's range
            or self.lower_bound > other.upper_bound
        )
