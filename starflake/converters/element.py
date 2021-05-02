from discord.ext import commands

from starflake.game_objects.element import Element


class ElementConverter(commands.Converter):
    """Select an element from the periodic table by its symbol."""

    async def convert(self, context, argument):
        for element in context.bot.periodic_table.elements:
            if element.symbol == argument:
                return element

        raise commands.BadArgument(f'"{argument}" is not an element symbol')
