import jsons
import discord
from discord.ext import commands

from starflake.game_objects.game import Game


class GameCog(commands.Cog, name="Game"):
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def new_game(self, context):
        """Set up a Starflake game in the current server."""

        # Shown in the audit log
        reason = f"{context.author.name} asked for a new game to be set up."

        category = await context.guild.create_category("Starflake", reason=reason)
        channel = await context.guild.create_text_channel("starflake", category=category, reason=reason)

        game = Game.new(category.id)
        game.save(context.bot)

        embed = discord.Embed(
            title="New game created",
            description=f"Go to {channel.mention} to start playing!",
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(GameCog())
