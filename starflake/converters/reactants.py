from discord.ext import commands

from starflake.converters.molecule import MoleculeConverter


class ReactantsConverter(commands.Converter):
    """Parse a list of reactants separated by +"""

    async def convert(self, context, argument):
        molecule_converter = MoleculeConverter()
        return [
            await molecule_converter.convert(context, molecule.strip())
            for molecule in argument.split("+")
        ]
