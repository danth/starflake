import discord
from discord.ext import commands

from starflake.converters.element import ElementConverter
from starflake.converters.molecule import MoleculeConverter
from starflake.game_objects.game import with_game


class InformationCog(commands.Cog, name="Information"):
    def cog_check(self, context):
        return with_game(context)

    @commands.command()
    async def periodic_table(self, context):
        """Display the game's periodic table."""

        await context.game.periodic_table.send_embed(context)

    @commands.command()
    async def elements(self, context):
        """Display a list of all elements."""

        embed = discord.Embed(title="Elements")

        for group_number, group in context.game.periodic_table.groups:
            element_list = "\n".join(f"{element.symbol}: {element.name}" for element in group)
            embed.add_field(name=f"Group {group_number}", value=element_list)

        await context.send(embed=embed)

    @commands.command()
    async def element(self, context, element: ElementConverter):
        """Display detailed information about an element."""

        await element.send_embed(context)

    @commands.command(aliases=["molecule"])
    async def compound(self, context, compound: MoleculeConverter):
        """Display detailed information about a compound."""

        await compound.send_embed(context)



def setup(bot):
    bot.add_cog(InformationCog())
