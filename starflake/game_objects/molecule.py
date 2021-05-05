import itertools

from starflake.utils import group_by
from starflake.game_objects.constants import SUBSCRIPTS


class BondingException(Exception):
    pass


class Molecule:
    """Multiple elements bonded together."""

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"{self.formula}:{len(self.colours)}"

    @property
    def name(self):
        """The full name of this molecule."""

        # TODO

    @property
    def formula(self):
        """The chemical formula of this molecule."""

        formula = ""

        for symbol, count in self.counted_symbols:
            formula += symbol
            if count > 1:
                formula += str(count).translate(SUBSCRIPTS)


        return formula

    @property
    def counted_symbols(self):
        """An iterator through (symbol, count) for all elements in the molecule."""

        grouped_elements = group_by(self.elements, lambda element: element.symbol)

        for symbol, elements in grouped_elements:
            yield symbol, len(list(elements))

    @property
    def colours(self):
        """The set of all colours present in this molecule."""

        return set.union(*(element.colours for element in self.elements))

    @property
    def mass(self):
        """The total mass of this molecule."""

        return sum(element.mass for element in self.elements)

    def can_bond(self, other):
        """Return whether these two molecules may be merged."""

        # Ensure each colour will only be present once in the new molecule
        # by checking the intersection is empty
        return len(self.colours & other.colours) == 0

    def __add__(self, other):
        """Merge these two molecules."""

        if not self.can_bond(other):
            raise BondingException(f"{self} cannot be bonded to {other}")

        return Molecule(self.elements + other.elements)


def react(elements):
    """Take a list of elements and return a list of synthesized molecules."""

    molecules = [Molecule([element]) for element in elements]

    while True:
        # Get all pairs of molecules
        pairs = itertools.combinations(molecules, 2)

        # Remove any pairs which aren't allowed to bond
        pairs = filter(lambda pair: Molecule.can_bond(*pair), pairs)

        # Find the pair with the highest total mass
        # (heavier molecules are more strongly attracted)
        pair = max(pairs, default=None, key=lambda pair: pair[0].mass + pair[1].mass)

        if pair is None:
            # No more bonds can be formed
            break

        # Remove the unbonded molecules
        molecules.remove(pair[0])
        molecules.remove(pair[1])

        # Insert the bonded molecule
        molecules.append(pair[0] + pair[1])

    return molecules
