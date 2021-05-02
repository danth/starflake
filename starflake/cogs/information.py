import discord
from discord.ext import commands

from starflake.converters.element import ElementConverter
from starflake.game_objects.colour import SATURATION, VALUE


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

        embed = discord.Embed(
            title=str(element).title(),
            colour=discord.Colour.from_hsv(
                element.spectrum.mean_hue,
                SATURATION,
                VALUE,
            ),
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Information())
