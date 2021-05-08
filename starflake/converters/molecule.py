from discord.ext import commands

from starflake.converters.element import ElementConverter
from starflake.game_objects import BondingException
from starflake.game_objects.molecule import Molecule


class MoleculeConverter(commands.Converter):
    """Construct a molecule from its formula."""

    async def convert(self, context, argument):
        element_converter = ElementConverter()
        molecule = None

        for index in range(0, len(argument), 2):
            # Convert each 2 characters to an element
            element_string = argument[index : index + 2]
            element = await element_converter.convert(context, element_string)

            if molecule is None:
                molecule = Molecule([element])
            else:
                try:
                    # Bond molecules to ensure the compound is legal
                    # (Rather than initialising a Molecule containing all the elements)
                    molecule += Molecule([element])
                except BondingException as exception:
                    # Convert to commands.BadArgument with the same message
                    raise commands.BadArgument(str(exception)) from exception

        return molecule
