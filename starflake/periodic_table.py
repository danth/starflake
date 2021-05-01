from starflake.element import Element


TABLE_WIDTH = 18
TABLE_HEIGHT = 7


class PeriodicTable:
    """A periodic table of elements."""

    @classmethod
    def random(cls):
        """Instantiate a periodic table of random elements."""

        elements = []
        # This list is used to prevent the same symbol being added twice
        symbols = []

        while len(elements) < (TABLE_WIDTH * TABLE_HEIGHT):
            element = Element.random()

            if element.symbol not in symbols:
                elements.append(element)
                symbols.append(element.symbol)

        return cls(elements)

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        # Display the element symbols in a grid
        return "\n".join(
            " ".join(
                element.symbol
                for element in row
            )
            for row in self.table
        )

    @property
    def table(self):
        """A 2d array containing all elements in a grid layout."""

        table = []

        for i in range(0, len(self.elements), TABLE_WIDTH):
            table.append(self.elements[i : i + TABLE_WIDTH])

        return table
