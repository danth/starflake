import random
from dataclasses import dataclass

import discord

from starflake.game_objects import RandomisableGameObject, EmbeddableGameObject
from starflake.game_objects.spectrum import Spectrum
from starflake.game_objects.constants import CONSONANTS, TABLE_GROUPS, VOWELS


@dataclass(repr=False, frozen=True)
class Element(RandomisableGameObject, EmbeddableGameObject):
    """A chemical element."""

    name: str
    symbol: str
    spectrum: Spectrum
    group_number: int
    period_number: int

    @classmethod
    def random(cls, group_number, period_number):
        """
        Instantiate a randomly named element.

        The given period number corresponds to the number of colours in the
        element's spectrum.
        """

        name = ""
        for _ in range(random.randint(2, 5)):
            # A consonant followed by a vowel is usually pronounceable
            name += random.choice(CONSONANTS)
            name += random.choice(VOWELS)

        # The symbol is the first two consonants in the name
        symbol = name[0].upper() + name[2]

        spectrum = Spectrum.random(period_number)

        return cls(name, symbol, spectrum, group_number, period_number)

    def __repr__(self):
        return self.symbol

    @property
    def mass(self):
        """The relative mass of this element."""

        return ((self.period_number - 1) * TABLE_GROUPS) + self.group_number

    async def send_embed(self, messageable):
        embed = discord.Embed(title=self.name.title())
        embed.add_field(name="Symbol", value=self.symbol)
        embed.add_field(name="Group", value=self.group_number)
        embed.add_field(name="Period", value=self.period_number)
        embed.add_field(name="Spectrum", value=self.spectrum.emoji, inline=False)
        await messageable.send(embed=embed)
