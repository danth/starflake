import discord
from discord.ext import commands

from starflake.converters.element import ElementConverter
from starflake.converters.molecule import MoleculeConverter
from starflake.game_objects.constants import COLOURS


def emoji_spectrum(colours):
    """Represent a spectrum using Discord emojis."""

    spectrum = ""

    for colour in COLOURS:
        if colour in colours:
            spectrum += f":{colour}_circle:"
        else:
            spectrum += "-"

    return spectrum


class Information(commands.Cog):
    @commands.command()
    async def periodic_table(self, context):
        """Display the game's periodic table."""

        embed = discord.Embed(
            title="Periodic Table",
            description=f"```\n{context.bot.periodic_table}\n```",
        )
        await context.send(embed=embed)

    @commands.command()
    async def elements(self, context):
        """Display a list of all elements."""

        embed = discord.Embed(title="Elements")

        for group_number, group in context.bot.periodic_table.groups:
            embed.add_field(
                name=f"Group {group_number}",
                value="\n".join(str(element).title() for element in group),
            )

        await context.send(embed=embed)

    @commands.command()
    async def element(self, context, element: ElementConverter):
        """Display detailed information about an element."""

        embed = discord.Embed(title=str(element).title())
        embed.add_field(name="Group", value=element.group_number)
        embed.add_field(name="Period", value=element.period_number)
        embed.add_field(name="Spectrum", value=emoji_spectrum(element.colours))
        await context.send(embed=embed)

    @commands.command(aliases=["molecule"])
    async def compound(self, context, compound: MoleculeConverter):
        """Display detailed information about a compound."""

        embed = discord.Embed(title=compound.name.title())
        embed.add_field(name="Formula", value=compound.formula)
        embed.add_field(
            name="Elements",
            value="\n".join(str(element).title() for element in compound.elements),
        )
        embed.add_field(name="Spectrum", value=emoji_spectrum(compound.colours))
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Information())
