from dataclasses import dataclass
from typing import List

import discord

from starflake.game_objects import RandomisableGameObject, EmbeddableGameObject
from starflake.game_objects.constants import TABLE_GROUPS, TABLE_PERIODS
from starflake.game_objects.element import Element
from starflake.utils import group_by


@dataclass(repr=False, frozen=True)
class PeriodicTable(RandomisableGameObject, EmbeddableGameObject):
    """A periodic table of elements."""

    elements: List[Element]

    @classmethod
    def random(cls):
        """Instantiate a periodic table of random elements."""

        elements = []
        # This list is used to prevent the same symbol being added twice
        symbols = []

        for period_number in range(1, TABLE_PERIODS + 1):
            for group_number in range(1, TABLE_GROUPS + 1):

                element = Element.random(group_number, period_number)
                while element.symbol in symbols:
                    # Choose a new element because this symbol is already used
                    element = Element.random(group_number, period_number)

                elements.append(element)
                symbols.append(element.symbol)

        return cls(elements)

    def __repr__(self):
        """Display the element symbols in a grid."""

        def format_number(number):
            return str(number).zfill(2)

        # Begin with a header like "   01 02 03 04 05 …"
        grid = (
            "   "
            + " ".join(format_number(group_number) for group_number, _ in self.groups)
            + "\n"
        )

        for period_number, period in self.periods:
            # Add the period number like "01 "
            grid += format_number(period_number) + " "
            # Add the symbols like "Ab Cd Ef Gh Ij …"
            grid += " ".join(element.symbol for element in period) + "\n"

        # Remove the trailing newline
        return grid.strip("\n")

    @property
    def periods(self):
        """An iterator through (period number, [elements]) for all periods."""

        return group_by(self.elements, lambda element: element.period_number)

    @property
    def groups(self):
        """An iterator through (group number, [elements]) for all groups."""

        return group_by(self.elements, lambda element: element.group_number)

    async def send_embed(self, messageable):
        embed = discord.Embed(title="Periodic Table", description=f"```\n{self}\n```")
        await messageable.send(embed=embed)
