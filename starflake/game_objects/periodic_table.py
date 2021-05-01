from starflake.game_objects.element import Element

GROUPS = 8
PERIODS = 5


class PeriodicTable:
    """A periodic table of elements."""

    @classmethod
    def random(cls):
        """Instantiate a periodic table of random elements."""

        elements = []
        # This list is used to prevent the same symbol being added twice
        symbols = []

        while len(elements) < (GROUPS * PERIODS):
            element = Element.random()

            if element.symbol not in symbols:
                elements.append(element)
                symbols.append(element.symbol)

        return cls(elements)

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        """Display the element symbols in a grid."""

        def format_index(index):
            return str(index + 1).zfill(2)

        # Begin with a header like "   01 02 03 04 05 …"
        grid = "   " + " ".join(map(format_index, range(GROUPS))) + "\n"

        for index, period in enumerate(self.periods):
            # Add the period number like "01 "
            grid += format_index(index) + " "
            # Add the symbols like "Ab Cd Ef Gh Ij …"
            grid += " ".join(element.symbol for element in period) + "\n"

        # Remove the trailing newline
        return grid.strip("\n")

    @property
    def periods(self):
        """A 2d array containing each period as a nested list."""

        periods = []

        for i in range(0, len(self.elements), GROUPS):
            periods.append(self.elements[i : i + GROUPS])

        return periods

    @property
    def groups(self):
        """A 2d array containing each group as a nested list."""

        # This transposes self.periods by zipping together the nth item from
        # each period, and converting the zipped tuples to lists
        return map(list, zip(*self.periods))
