import discord
from discord.ext import commands


class Information(commands.Cog):
    @commands.command()
    async def periodic_table(self, context):
        """Display the game's periodic table."""

        embed = discord.Embed(
            title="Periodic Table",
            description=f"```\n{context.bot.periodic_table}\n```",
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Information())
