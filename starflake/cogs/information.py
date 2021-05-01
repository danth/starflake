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

    @commands.command()
    async def elements(self, context):
        """Display a list of all elements."""

        embed = discord.Embed(title="Elements")

        for i, group in enumerate(context.bot.periodic_table.groups):
            embed.add_field(
                name=f"Group {i + 1}",
                value="\n".join(str(element).title() for element in group),
            )

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Information())
