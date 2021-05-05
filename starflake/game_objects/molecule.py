import itertools

from starflake.utils import group_by

SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


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

    def merge(self, other):
        """Merge these two molecules, or return None if not permitted."""

        # Ensure each colour will only be present once in the new molecule
        # (If the intersection is non-empty, this will be True)
        if self.colours & other.colours:
            return None

        return Molecule(self.elements + other.elements)


def react(elements):
    """Take a list of elements and return a list of synthesized molecules."""

    molecules = [Molecule([element]) for element in elements]

    while True:
        # Find the first pair which are able to merge
        for molecule_a, molecule_b in itertools.combinations(molecules, 2):
            merged = molecule_a.merge(molecule_b)
            if merged:
                molecules.remove(molecule_a)
                molecules.remove(molecule_b)
                molecules.append(merged)
                break
        else:
            # If we didn't break, no merge was made so another pass is unnecessary
            break

    return molecules
