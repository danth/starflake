import discord
from discord.ext import commands

from starflake.converters.element import ElementConverter
from starflake.converters.molecule import MoleculeConverter
from starflake.converters.reactants import ReactantsConverter
from starflake.game_objects.game import with_game
from starflake.game_objects.molecule import react


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
            element_list = "\n".join(
                f"{element.symbol}: {element.name}" for element in group
            )
            embed.add_field(name=f"Group {group_number}", value=element_list)

        await context.send(embed=embed)

    @commands.command()
    async def element(self, context, *, element: ElementConverter):
        """
        Display detailed information about an element.

        Specify the element's symbol, not its name.
        """

        await element.send_embed(context)

    @commands.command(aliases=["molecule"])
    async def compound(self, context, *, compound: MoleculeConverter):
        """
        Display detailed information about a compound.

        Specify the compound's formula, not its name.
        """

        await compound.send_embed(context)

    @commands.command()
    async def products(self, context, *, reactants: ReactantsConverter):
        """
        Determine the products of a reaction.

        Specify the reactants as their symbol or formula, not their name,
        and separate each reactant with a `+`.
        """

        products = react(reactants)

        for product in products:
            await product.send_embed(context)


def setup(bot):
    bot.add_cog(InformationCog())
