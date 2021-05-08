import itertools

import discord

from starflake.game_objects import BondableGameObject, EmbeddableGameObject
from starflake.game_objects.spectrum import Spectrum


class Molecule(EmbeddableGameObject, BondableGameObject):
    """Multiple elements bonded together."""

    def __init__(self, elements):
        self.elements = elements

        # Keep elements in alphabetical order by symbol
        self.elements.sort(key=lambda element: element.symbol)

    def __repr__(self):
        return self.formula

    @property
    def name(self):
        """The full name of this molecule."""

        names = [element.name for element in self.elements]

        def add_suffix(suffix):
            return " ".join(names[:-1]) + " " + names[-1][:-1] + suffix

        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return add_suffix("ide")
        if len(names) == 3:
            return add_suffix("ate")
        if len(names) == 4:
            return add_suffix("ite")
        return add_suffix("oplex")

    @property
    def formula(self):
        """The chemical formula of this molecule."""

        symbols = [element.symbol for element in self.elements]
        return "".join(symbols)

    @property
    def mass(self):
        """The total mass of this molecule."""

        return sum(element.mass for element in self.elements)

    @property
    def spectrum(self):
        """The overall spectrum of this molecule."""

        return Spectrum.bond_many([element.spectrum for element in self.elements])

    def can_bond(self, other):
        return self.spectrum.can_bond(other.spectrum)

    def bond(self, other):
        return Molecule(self.elements + other.elements)

    async def send_embed(self, messageable):
        embed = discord.Embed(title=self.name.title())
        embed.add_field(name="Formula", value=self.formula)
        element_list = "\n".join(
            f"{element.symbol}: {element.name}" for element in self.elements
        )
        embed.add_field(name="Elements", value=element_list)
        embed.add_field(name="Spectrum", value=self.spectrum.emoji, inline=False)
        await messageable.send(embed=embed)


def react(reactants):
    """Take a list of molecules and perform a reaction between them."""

    # Break down the original molecules
    elements = []
    for reactant in reactants:
        elements += reactant.elements

    # Create new molecules with 1 element each
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
